"""
BirthVerse — Your Birthday Story & World History Explorer
Python Web Server.

Run with:
    python3 app.py
Then open http://localhost:8080 in your browser.
"""

from __future__ import annotations
import os
import sys
import json
import random
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any

from birthday_engine import compute_birthday_profile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "index.html")
STATIC_DIR = os.path.join(BASE_DIR, "static")

PRESET_DATES = [
    {"label": "Apollo 11 Moon Landing", "date": "1969-07-20", "time": "20:17", "name": "Apollo 11 Explorer"},
    {"label": "World Wide Web Public Debut", "date": "1991-08-06", "time": "09:00", "name": "Web Pioneer"},
    {"label": "Millennium Turn (Y2K)", "date": "2000-01-01", "time": "00:00", "name": "Millennium Child"},
    {"label": "First iPhone Launch Year", "date": "2007-01-09", "time": "09:41", "name": "Digital Native"},
    {"label": "Fall of the Berlin Wall", "date": "1989-11-09", "time": "18:53", "name": "History Witness"},
]


def handle_analyze_request(params: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    date_str = str(params.get("date", "")).strip()
    time_str = str(params.get("time", "00:00")).strip() or "00:00"
    name_str = str(params.get("name", "")).strip()

    if not date_str:
        return 400, {"error": "Please select or enter a valid birth date (YYYY-MM-DD)."}

    try:
        profile = compute_birthday_profile(
            birth_date_str=date_str,
            birth_time_str=time_str,
            user_name=name_str,
            try_live_history=True,
        )
        return 200, {"ok": True, "data": profile}
    except ValueError as exc:
        return 400, {"ok": False, "error": str(exc)}
    except Exception as exc:
        return 500, {"ok": False, "error": f"Unexpected calculation error: {exc}"}


def generate_random_birthday() -> dict[str, str]:
    year = random.randint(1955, 2012)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.choice([0, 15, 30, 45])
    return {
        "date": f"{year:04d}-{month:02d}-{day:02d}",
        "time": f"{hour:02d}:{minute:02d}",
        "name": "Time Traveler",
    }


class ChronosHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Standard-library HTTP handler with REST API & static file serving."""

    def log_message(self, format: str, *args: Any) -> None:
        sys.stdout.write(f"[Chronos] {self.address_string()} - {format % args}\n")

    def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_path: str) -> None:
        with open(html_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._send_html(TEMPLATE_PATH)
            return

        if path == "/api/analyze":
            qs = urllib.parse.parse_qs(parsed.query)
            params = {k: v[0] for k, v in qs.items() if v}
            status, payload = handle_analyze_request(params)
            self._send_json(status, payload)
            return

        if path == "/api/presets":
            self._send_json(200, {"ok": True, "presets": PRESET_DATES})
            return

        if path == "/api/random":
            rnd = generate_random_birthday()
            status, payload = handle_analyze_request(rnd)
            self._send_json(status, payload)
            return

        if path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            safe_path = os.path.normpath(os.path.join(STATIC_DIR, rel_path))
            if safe_path.startswith(STATIC_DIR) and os.path.isfile(safe_path):
                ext = os.path.splitext(safe_path)[1].lower()
                mime_map = {
                    ".css": "text/css; charset=utf-8",
                    ".js": "application/javascript; charset=utf-8",
                    ".svg": "image/svg+xml",
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".ico": "image/x-icon",
                }
                ctype = mime_map.get(ext, "application/octet-stream")
                with open(safe_path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

        self.send_error(404, "File not found")

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/analyze":
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            try:
                params = json.loads(raw_body)
            except json.JSONDecodeError:
                params = {}
            status, payload = handle_analyze_request(params)
            self._send_json(status, payload)
            return

        self.send_error(404, "Endpoint not found")


def run_server(port: int = 8080, host: str = "127.0.0.1") -> None:
    server = HTTPServer((host, port), ChronosHTTPRequestHandler)
    print(f"\n✨ BirthVerse — Your Birthday Story & World History Explorer ✨")
    print(f"🚀 Server running at: http://{host}:{port}")
    print("Press Ctrl+C to stop the server.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get("HOST", "127.0.0.1")
    run_server(port=port, host=host)

