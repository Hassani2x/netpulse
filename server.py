import json
import subprocess
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class NetPulseHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/check":
            try:
                result = subprocess.run(
                    ["ping", "-c", "1", "127.0.0.1"],
                    capture_output=True,
                    timeout=5
                )
                reachable = result.returncode == 0
            except subprocess.TimeoutExpired:
                reachable = False

            response = json.dumps({
                "ip": "127.0.0.1",
                "reachable": reachable
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response)
        else:
            super().do_GET()


project_folder = Path(__file__).resolve().parent
handler = partial(NetPulseHandler, directory=str(project_folder))
server = HTTPServer(("127.0.0.1", 8000), handler)

print("NetPulse is running at http://127.0.0.1:8000")
server.serve_forever()
