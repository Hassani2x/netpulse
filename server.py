import json
import subprocess
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ALLOWED_IPS = {"127.0.0.1", "192.168.1.1"}


class NetPulseHandler(SimpleHTTPRequestHandler):
    def send_json(self, data, status_code=200):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        url = urlsplit(self.path)

        if url.path != "/check":
            super().do_GET()
            return

        parameters = parse_qs(url.query)
        ip_address = parameters.get("ip", ["127.0.0.1"])[0]

        if ip_address not in ALLOWED_IPS:
            self.send_json({
                "error": "Choose 127.0.0.1 or 192.168.1.1."
            }, 400)
            return

        try:
            result = subprocess.run(
                ["ping", "-c", "1", ip_address],
                capture_output=True,
                timeout=5
            )

            outcome = "reply" if result.returncode == 0 else "no_reply"

        except subprocess.TimeoutExpired:
            outcome = "timeout"

        except OSError:
            self.send_json({
                "error": "Python could not start ping."
            }, 500)
            return

        self.send_json({
            "ip": ip_address,
            "reachable": outcome == "reply",
            "outcome": outcome
        })


project_folder = Path(__file__).resolve().parent
handler = partial(NetPulseHandler, directory=str(project_folder))
server = HTTPServer(("127.0.0.1", 8000), handler)

print("NetPulse is running at http://127.0.0.1:8000")
server.serve_forever()
