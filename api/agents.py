"""Vercel serverless function: agents REST (GET /api/agents[/:slug]).

Thin wrapper over api/_core.py -- all logic lives there. Stdlib only.
Same auth as MCP: 401 without a valid Bearer token. Directory only -- this
server lists agents, it does not run agent loops. The vercel.json rewrite
maps /api/agents/:slug to /api/agents?slug=:slug; handle_rest accepts the
slug from either the path or the query string.
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
            "GET", parsed.path or "/api/agents", query,
            self.headers.get("Authorization") or "")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
