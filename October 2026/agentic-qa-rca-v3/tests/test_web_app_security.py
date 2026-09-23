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
    def test_batch_trace_report_uses_session_report_and_evidence_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "data" / "output").mkdir(parents=True)
            (root / "evidence").mkdir()
            context_path = root / "context.yaml"
            input_path = root / "input.json"
            session_path = root / "session-under-test.json"
            with patch.object(web_app, "PROJECT_ROOT", root), patch.object(
                web_app, "WRITE_ALLOWLIST", (root / "data" / "output", root / "evidence")
            ), patch.object(web_app, "run") as batch_run:
                report_path = web_app._create_batch_trace_report(context_path, input_path, session_path)

            expected_report = root / "data" / "output" / "report_session-under-test.json"
            expected_evidence = root / "evidence" / "evidence_log.csv"
            self.assertEqual(report_path, expected_report.resolve())
            batch_run.assert_called_once_with(
                context_path=context_path,
                input_path=input_path,
                output_path=expected_report.resolve(),
                evidence_log_path=expected_evidence.resolve(),
            )

    def test_default_evidence_log_is_write_permitted(self):
        path = web_app._resolve_path("", default=Path("evidence/evidence_log.csv"), access="write")
        self.assertEqual(path, (web_app.PROJECT_ROOT / "evidence" / "evidence_log.csv").resolve())

    def test_start_and_quick_plan_include_batch_report_path(self):
        handler = object.__new__(web_app.RcaWebHandler)
        handler.request_id = "test-request"
        handler.wfile = io.BytesIO()
        handler.sent_headers = {}
        handler.response_status = 200
        handler.send_response = lambda status: setattr(handler, "response_status", status)
        handler.send_header = lambda name, value: handler.sent_headers.__setitem__(name, value)
        handler.end_headers = lambda: None

        session = {"status": "awaiting_answer"}
        report_path = Path("data/output/report_synthetic.json")
        with patch.object(web_app, "_resolve_path", return_value=Path("synthetic.json")), patch.object(
            web_app, "_load_context_bundle", return_value=({}, {})
        ), patch.object(web_app, "start_session", return_value=session), patch.object(
            web_app, "_discover_evidence_refs", return_value=[]
        ), patch.object(web_app, "_create_batch_trace_report", return_value=report_path):
            handler._handle_start(
                {"context": "context.yaml", "input": "input.json", "defect_id": "DEF-SYN", "session": "session.json"}
            )
        start_response = json.loads(handler.wfile.getvalue())
        self.assertEqual(start_response["batch_report_path"], web_app._rel(report_path))

        handler.wfile = io.BytesIO()
        with patch.object(web_app, "_resolve_path", return_value=Path("synthetic.json")), patch.object(
            web_app, "_load_quick_plan", return_value={"answers": []}
        ), patch.object(web_app, "run_guided_rca", return_value={}), patch.object(
            web_app, "load_session_status", return_value=session
        ), patch.object(web_app, "_discover_evidence_refs", return_value=[]), patch.object(
            web_app, "_create_batch_trace_report", return_value=report_path
        ):
            handler._handle_run_quick_plan(
                {
                    "context": "context.yaml",
                    "input": "input.json",
                    "defect_id": "DEF-SYN",
                    "session": "session.json",
                    "quick_plan": "quick-plan.json",
                    "output_report": "report.md",
                }
            )
        quick_response = json.loads(handler.wfile.getvalue())
        self.assertEqual(quick_response["batch_report_path"], web_app._rel(report_path))

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