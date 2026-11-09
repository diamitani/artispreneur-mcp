"""Vercel serverless function: packs REST (GET /api/packs).

Thin wrapper over api/_core.py -- all logic lives there. Stdlib only.
Same auth as MCP: 401 without a valid Bearer token. The 4 Artispreneur
packs (Free $0, All-Access $20/mo, Pro $200/mo, Label $25/seat/mo) with
stripe_status "not_live_in_this_package" -- Stripe is not live here.
"""
import importlib.util
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "artispreneur_core", os.path.join(_HERE, "_core.py"))
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)


class handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        status, ctype, body = core.handle_rest(
            "GET", parsed.path or "/api/packs", query,
            self.headers.get("Authorization") or "")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
