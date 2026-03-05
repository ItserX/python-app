import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class SimpleHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            self._send_json({"message": "Hello from simple Python server"})
        elif self.path == "/health":
            self._send_json({"status": "ok"})
        else:
            self._send_json({"error": "Not found"}, status=404)

    def log_message(self, format: str, *args) -> None:
        # Disable default noisy HTTP request logs in tests and local runs.
        return



def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = HTTPServer((host, port), SimpleHandler)
    print(f"Server started at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Server stopped")


if __name__ == "__main__":
    env_host = os.getenv("APP_HOST", "127.0.0.1")
    env_port = int(os.getenv("APP_PORT", "8000"))
    run_server(host=env_host, port=env_port)
