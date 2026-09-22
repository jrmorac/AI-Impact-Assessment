import csv
import hashlib
import http.client
import io
import json
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import web_app


class ExportGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.read_root = self.root / "read"
        self.write_root = self.root / "write"
        self.read_root.mkdir()
        self.write_root.mkdir()
        self.session_path = self.read_root / "synthetic-session.json"
        self.session_path.write_text(
            json.dumps(
                {
                    "session_id": "synthetic-session",
                    "status": "root_cause_confirmed",
                    "defect": {
                        "defect_id": "SYN-001",
                        "component": "SyntheticComponent",
                        "summary": "Synthetic transfer failed",
                        "expected_behavior": "The transfer creates the outbound file.",
                        "observed_behavior": "The outbound file was not created.",
                    },
                    "category": "capacity",
                    "root_cause_summary": "Synthetic capacity control rejected the transfer",
                    "stop_reason": "Synthetic evidence confirmed the cause.",
                    "next_action": "Validate the corrective control.",
                    "why_chain": [
                        {"why_index": 1, "question": "Why?", "answer": "Synthetic cause", "evidence_refs": ["synthetic.log"]}
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.patches = [
            patch.object(web_app, "PROJECT_ROOT", self.root),
            patch.object(web_app, "READ_ALLOWLIST", (self.read_root,)),
            patch.object(web_app, "WRITE_ALLOWLIST", (self.write_root,)),
        ]
        for item in self.patches:
            item.start()
        web_app._EXPORT_PREVIEWS.clear()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), web_app.RcaWebHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        for item in reversed(self.patches):
            item.stop()
        self.temp_dir.cleanup()

    def post(self, path, payload):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        body = json.dumps(payload).encode("utf-8")
        connection.request("POST", path, body=body, headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        result = json.loads(response.read().decode("utf-8"))
        request_id = response.getheader("X-Request-ID")
        connection.close()
        return response.status, result, request_id

    def preview(self, kind, output_name):
        return self.post(
            "/api/export-preview",
            {"kind": kind, "session": str(self.session_path), "output": str(self.write_root / output_name)},
        )

    def commit(self, preview, **options):
        return self.post(
            "/api/export-commit",
            {
                "preview_id": preview["preview_id"],
                "approved": True,
                "content_sha256": preview["content_sha256"],
                **options,
            },
        )

    def test_preview_is_side_effect_free_for_all_kinds(self):
        for kind, name in (("report", "report.md"), ("capa", "capa.csv"), ("ado", "ado.csv")):
            status, result, request_id = self.preview(kind, name)
            self.assertEqual(status, 200)
            self.assertTrue(request_id)
            self.assertEqual(result["byte_count"], len(result["content"].encode("utf-8")))
            self.assertEqual(result["content_sha256"], hashlib.sha256(result["content"].encode("utf-8")).hexdigest())
            self.assertFalse((self.write_root / name).exists())

    def test_commit_requires_approval_and_writes_atomically(self):
        _, preview, _ = self.preview("report", "approved.md")
        status, _, _ = self.post(
            "/api/export-commit",
            {"preview_id": preview["preview_id"], "content_sha256": preview["content_sha256"]},
        )
        self.assertEqual(status, 400)
        self.assertFalse((self.write_root / "approved.md").exists())

        status, result, request_id = self.commit(preview)
        self.assertEqual(status, 200)
        self.assertTrue(request_id)
        output = self.write_root / "approved.md"
        self.assertEqual(result["committed_path"], "write/approved.md")
        self.assertEqual(output.read_text(encoding="utf-8"), preview["content"])
        self.assertFalse(list(self.write_root.glob(".approved.md.*")))

    def test_existing_target_requires_explicit_overwrite(self):
        output = self.write_root / "conflict.csv"
        output.write_text("original\n", encoding="utf-8")
        _, preview, _ = self.preview("capa", "conflict.csv")
        status, _, _ = self.commit(preview)
        self.assertEqual(status, 409)
        self.assertEqual(output.read_text(encoding="utf-8"), "original\n")

        _, replacement, _ = self.preview("capa", "conflict.csv")
        status, _, _ = self.commit(replacement, overwrite=True)
        self.assertEqual(status, 200)
        self.assertNotEqual(output.read_text(encoding="utf-8"), "original\n")

    def test_hash_mismatch_and_stale_preview_are_conflicts(self):
        _, preview, _ = self.preview("ado", "stale.csv")
        status, _, _ = self.post(
            "/api/export-commit",
            {"preview_id": preview["preview_id"], "approved": True, "content_sha256": "0" * 64},
        )
        self.assertEqual(status, 409)
        web_app._EXPORT_PREVIEWS[preview["preview_id"]]["expires_epoch"] = 0
        status, _, _ = self.commit(preview)
        self.assertEqual(status, 409)

    def test_traversal_is_rejected(self):
        status, result, _ = self.post(
            "/api/export-preview",
            {"kind": "report", "session": str(self.session_path), "output": str(self.write_root / ".." / "escape.md")},
        )
        self.assertEqual(status, 400)
        self.assertEqual(result["error_code"], "PATH_NOT_ALLOWED")

    def test_all_committed_formats_are_valid(self):
        cases = (("report", "valid.md"), ("capa", "valid-capa.csv"), ("ado", "valid-ado.csv"))
        for kind, name in cases:
            _, preview, _ = self.preview(kind, name)
            status, _, _ = self.commit(preview)
            self.assertEqual(status, 200)
            output = self.write_root / name
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), preview["content_sha256"])
            if kind == "report":
                self.assertTrue(output.read_text(encoding="utf-8").startswith("# RCA Case Report"))
            else:
                rows = list(csv.reader(io.StringIO(output.read_text(encoding="utf-8"))))
                self.assertGreaterEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()