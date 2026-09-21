import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import web_app


class FakeHandler:
    def __init__(self, body: bytes = b"{}", content_type: str = "application/json"):
        self.headers = {"Content-Length": str(len(body)), "Content-Type": content_type}
        self.rfile = io.BytesIO(body)
        self.wfile = io.BytesIO()
        self.request_id = "test-request"
        self.response_status = 200
        self.sent_headers = {}

    def send_response(self, status):
        self.response_status = status

    def send_header(self, name, value):
        self.sent_headers[name] = value

    def end_headers(self):
        pass


class WebAppSecurityTests(unittest.TestCase):
    def test_read_and_write_allowlists_reject_traversal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            read_root = root / "read"
            write_root = root / "write"
            read_root.mkdir()
            write_root.mkdir()
            with patch.object(web_app, "READ_ALLOWLIST", (read_root,)), patch.object(
                web_app, "WRITE_ALLOWLIST", (write_root,)
            ):
                self.assertEqual(
                    web_app._resolve_path(str(read_root / "file.json")),
                    (read_root / "file.json").resolve(),
                )
                self.assertEqual(
                    web_app._resolve_path(str(write_root / "file.json"), access="write"),
                    (write_root / "file.json").resolve(),
                )
                with self.assertRaises(web_app.PathPolicyError):
                    web_app._resolve_path("../outside.json")
                with self.assertRaises(web_app.PathPolicyError):
                    web_app._resolve_path("read/file.json", access="write")

    def test_symlink_target_must_remain_in_allowlist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            read_root = root / "read"
            outside = root / "outside"
            read_root.mkdir()
            outside.mkdir()
            link = read_root / "link.json"
            try:
                link.symlink_to(outside / "secret.json")
            except OSError as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            with patch.object(web_app, "READ_ALLOWLIST", (read_root,)):
                with self.assertRaises(web_app.PathPolicyError):
                    web_app._resolve_path(str(link))

    def test_false_string_is_false(self):
        self.assertFalse(web_app._parse_bool("false", default=True))
        self.assertTrue(web_app._parse_bool("true", default=False))

    def test_body_requires_json_and_respects_limit(self):
        with self.assertRaises(web_app.RequestBodyError):
            web_app._read_json_body(FakeHandler(b"{}", "text/plain"))
        with patch.object(web_app, "MAX_REQUEST_BODY_BYTES", 2):
            with self.assertRaises(web_app.RequestBodyError):
                web_app._read_json_body(FakeHandler(b"{}x"))

    def test_json_response_contains_request_id_without_payload_logging(self):
        handler = FakeHandler()
        web_app._json_response(handler, 200, {"status": "ok"})
        response = json.loads(handler.wfile.getvalue())
        self.assertEqual(response, {"status": "ok", "request_id": "test-request"})


if __name__ == "__main__":
    unittest.main()