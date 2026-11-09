#!/usr/bin/env python3
"""Artispreneur MCP + REST API -- local runner (v1).

Thin HTTP shell over api/_core.py (all logic lives there, shared with the
Vercel functions). Stdlib only.

Routes:
  POST   /mcp          JSON-RPC (Streamable HTTP); initialize mints a session
  GET    /mcp          SSE keep-alive (valid session required; local only --
                       Vercel returns 405, POST is the transport there)
  DELETE /mcp          terminate the session
  GET    /health       public liveness probe (counts, no secrets)
  GET    /             public human-readable info
  GET    /api/skills           list (tenant/query/category/page/per_page)
  GET    /api/skills/:slug     one skill body (same gating as get_skill)
  GET    /api/agents           list the 7 music agents
  GET    /api/agents/:slug     one agent
  GET    /api/packs            the 4 Artispreneur packs

Auth: Bearer token on /mcp and every /api route except /health.
HOST defaults to 127.0.0.1 (never 0.0.0.0 by default -- QA W-2 fix);
set HOST=0.0.0.0 explicitly only inside the Dockerfile. PORT env, 8787.

Run:  python3 server.py
"""
import importlib.util
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_spec = importlib.util.spec_from_file_location(
    "artispreneur_core", os.path.join(HERE, "api", "_core.py"))
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)

HOST = core.HOST
PORT = core.PORT


def _lower_headers(handler):
    return {k.lower(): v for k, v in handler.headers.items()}


def _flat_query(qs):
    return {k: v[0] for k, v in parse_qs(qs).items()}


class Handler(BaseHTTPRequestHandler):
    server_version = "ArtispreneurMCP/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("[artispreneur-mcp] " + fmt % args + "\n")

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
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/mcp":
            # Local SSE keep-alive. Vercel does NOT serve this (405 there).
            ent, reason = core._resolve_bearer(
                self.headers.get("Authorization") or "")
            if ent is None:
                self._send(401, {"Content-Type": "application/json"},
                           core._unauthorized_body(reason))
                return
            sid = self.headers.get("Mcp-Session-Id")
            if not sid or not core._valid_session(sid):
                # A strict client may open the GET stream before it has a
                # session (e.g. before POST initialize). Mint one instead of
                # 400ing: the client learns it from the response header.
                sid = core._new_session()
                self.send_response(200)
                self._cors()
                self.send_header("Mcp-Session-Id", sid)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.end_headers()
                try:
                    while core._valid_session(sid):
                        self.wfile.write(b": ping\n\n")
                        self.wfile.flush()
                        time.sleep(25)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            try:
                while core._valid_session(sid):
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    time.sleep(25)
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        status, ctype, body = core.handle_rest(
            "GET", path, _flat_query(parsed.query),
            self.headers.get("Authorization") or "",
            host=self.headers.get("Host") or "")
        self._send(status, {"Content-Type": ctype}, body)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path != "/mcp":
            self.send_response(404)
            self._cors()
            self.end_headers()
            return
        status, headers, body = core.handle_mcp_delete(_lower_headers(self))
        self._send(status, headers, body)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/mcp":
            self.send_response(404)
            self._cors()
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        status, headers, body = core.handle_mcp_post(raw, _lower_headers(self))
        self._send(status, headers, body)


def main():
    print("Loaded library=%d artispreneur active=%d draft=%d packs=%d agents=%d"
          % (core.COUNTS["library"], core.COUNTS["artispreneur_active"],
             core.COUNTS["artispreneur_draft"], core.COUNTS["packs"],
             core.COUNTS["agents"]), flush=True)
    print("Auth: admin token %s; demo entitlement keys: %d (DEMO ONLY, "
          "never deploy as-shipped)"
          % ("SET" if core.MCP_AUTH_TOKEN else "NOT SET",
             len(core._entitlements)), flush=True)
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print("Serving Artispreneur MCP on http://%s:%d/mcp" % (HOST, PORT), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
