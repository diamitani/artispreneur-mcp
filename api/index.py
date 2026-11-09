"""Vercel serverless function: human landing page for GET /.

Thin wrapper over api/_core.py -- all logic lives there. Stdlib only.
Public: no auth. A browser tapping the root URL must see this HTML page,
never a JSON error or a 404. The MCP endpoint itself is POST /mcp.
"""
import importlib.util
import os
from http.server import BaseHTTPRequestHandler

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "artispreneur_core", os.path.join(_HERE, "_core.py"))
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)


class handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        body = core.landing_html(
            core.BASE_URL, self.headers.get("Host") or "").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
