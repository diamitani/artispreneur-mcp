"""Vercel serverless function: MCP endpoint (POST /mcp).

Thin wrapper over api/_core.py -- all logic lives there. Stdlib only.

Vercel statelessness: serverless functions cannot hold sessions or SSE
across invocations. So:
  - POST /mcp is the transport. initialize returns a session id, but
    tools/call ACCEPTS a missing or unknown session id (lenient/stateless
    mode -- auth is the Bearer token, not the session). Only a session id
    explicitly torn down with DELETE /mcp is rejected.
  - GET /mcp returns a BOUNDED SSE stream (200 text/event-stream): an
    immediate ping, then a ping every 5s for up to SSE_HOLD_SECONDS
    (default 20, env-overridable, capped at 50), then the stream closes
    cleanly. This is best-effort only: the Vercel Python runtime may
    buffer the response until the handler returns, so a strict client
    that needs a live long-lived stream should use the Render host
    instead (server.py holds the stream open with a 25s ping loop and
    real sessions). The old 405 is gone — no client should see a
    method-not-allowed error for GET /mcp any more.
  - DELETE /mcp tears the session down (in-process only).
  - The usage ledger defaults to /tmp/usage_ledger.jsonl on Vercel
    (ephemeral); ledger writes never fail a call.
  - entitlements.json is NOT deployed (excluded in vercel.json), so only
    the MCP_AUTH_TOKEN admin key authenticates on Vercel until the
    Supabase has_access() lookup replaces demo entitlements (go-live step).
"""
import importlib.util
import json
import os
import time
from http.server import BaseHTTPRequestHandler

# Bounded SSE hold for GET /mcp on Vercel. Keep well under the Hobby
# function duration limit; a strict long-lived SSE client belongs on Render.
SSE_HOLD_SECONDS = max(5, min(50, int(os.environ.get("SSE_HOLD_SECONDS", "20"))))
SSE_PING_EVERY = 5

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "artispreneur_core", os.path.join(_HERE, "_core.py"))
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)


def _lower_headers(handler):
    return {k.lower(): v for k, v in handler.headers.items()}


class handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers",
                         "Content-Type, Accept, Mcp-Session-Id, MCP-Protocol-Version, Authorization")
        self.send_header("Access-Control-Expose-Headers", "Mcp-Session-Id")

    def _send(self, status, headers, body):
        self.send_response(status)
        self._cors()
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        if body is not None:
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()

    def do_GET(self):
        # Bounded SSE stream (see module docstring). Auth first, exactly
        # like POST; session is lenient (Vercel cannot hold one anyway).
        ent, reason = core._resolve_bearer(
            self.headers.get("Authorization") or "")
        if ent is None:
            self._send(401, {"Content-Type": "application/json"},
                       core._unauthorized_body(reason))
            return
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        sid = self.headers.get("Mcp-Session-Id")
        if sid:
            self.send_header("Mcp-Session-Id", sid)
        self.end_headers()
        # Immediate ping, then one every 5s until the hold expires. A
        # client that needs a live stream past this window reconnects or
        # continues over POST; the stream closes cleanly, never 405.
        deadline = time.time() + SSE_HOLD_SECONDS
        try:
            while True:
                self.wfile.write(b": ping\n\n")
                self.wfile.flush()
                if time.time() + SSE_PING_EVERY > deadline:
                    break
                time.sleep(SSE_PING_EVERY)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_DELETE(self):
        status, headers, body = core.handle_mcp_delete(_lower_headers(self))
        self._send(status, headers, body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        status, headers, body = core.handle_mcp_post(raw, _lower_headers(self))
        self._send(status, headers, body)
