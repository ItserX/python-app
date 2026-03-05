import http.client
import json
import threading
import time
import unittest
from http.server import HTTPServer

from app.server import SimpleHandler


class ServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = HTTPServer(("127.0.0.1", 0), SimpleHandler)
        cls.host, cls.port = cls.server.server_address
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

        # Small pause to make sure server is ready before first request.
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=1)

    def _get(self, path: str):
        conn = http.client.HTTPConnection(self.host, self.port, timeout=2)
        try:
            conn.request("GET", path)
            response = conn.getresponse()
            body = response.read().decode("utf-8")
            data = json.loads(body)
            return response.status, data
        finally:
            conn.close()

    def test_root_endpoint(self):
        status, data = self._get("/")
        self.assertEqual(status, 200)
        self.assertEqual(data, {"message": "Hello from simple Python server"})

    def test_health_endpoint(self):
        status, data = self._get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(data, {"status": "ok"})

    def test_not_found(self):
        status, data = self._get("/missing")
        self.assertEqual(status, 404)
        self.assertEqual(data, {"error": "Not found"})


if __name__ == "__main__":
    unittest.main()
