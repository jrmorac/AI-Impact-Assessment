from __future__ import annotations

import argparse
import hashlib
import html
import json
import logging
import os
import tempfile
import threading
import time
import traceback
import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

from io_utils import load_json
from interactive_rca import answer_session, load_session_status, render_report_markdown, revise_current_answer, start_session
from main import (
    _load_quick_plan,
    _default_report_path,
    _default_session_path,
    _discover_evidence_refs,
    _load_context_bundle,
    render_ado_testcases_csv,
    render_capa_csv,
    run,
    run_guided_rca,
    run_demo,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEB_ROOT = PROJECT_ROOT / "web"
READ_ALLOWLIST = (
    PROJECT_ROOT / "project-context",
    PROJECT_ROOT / "data" / "input",
    PROJECT_ROOT / "data" / "output",
    PROJECT_ROOT / "evidence",
    WEB_ROOT,
)
WRITE_ALLOWLIST = (
    PROJECT_ROOT / "data" / "output",
    PROJECT_ROOT / "evidence" / "rca_sessions",
    PROJECT_ROOT / "evidence" / "rca_reports",
    PROJECT_ROOT / "evidence" / "capa_exports",
    PROJECT_ROOT / "evidence" / "evidence_log.csv",
)
CAPA_PROVIDERS = {"ado", "jira", "generic"}
ADO_VARIANT_SETS = {"standard", "expanded"}
MAX_REQUEST_BODY_BYTES = 1_048_576
EXPORT_PREVIEW_TTL_SECONDS = 900
_EXPORT_PREVIEWS: Dict[str, Dict[str, Any]] = {}
_EXPORT_PREVIEWS_LOCK = threading.Lock()
LOGGER = logging.getLogger("agentic_qa.web")
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False
if not LOGGER.handlers:
    _log_handler = logging.StreamHandler()
    _log_handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(_log_handler)


class PathPolicyError(ValueError):
    pass


class RequestValidationError(ValueError):
    pass


class RequestBodyError(ValueError):
    pass


class ExportConflictError(ValueError):
    pass


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _is_within(path: Path, roots: tuple[Path, ...]) -> bool:
    return any(path == root or root in path.parents for root in roots)


def _resolve_path(raw: str, *, default: Path | None = None, access: str = "read") -> Path:
    if access not in {"read", "write"}:
        raise ValueError("Invalid path access mode")
    candidate = raw.strip() if raw else ""
    if not candidate:
        if default is None:
            raise RequestValidationError("Path value is required")
        path = (PROJECT_ROOT / default) if not default.is_absolute() else default
    else:
        path = Path(candidate)
        if not path.is_absolute():
            path = PROJECT_ROOT / path

    resolved = path.resolve(strict=False)
    roots = READ_ALLOWLIST if access == "read" else WRITE_ALLOWLIST
    resolved_roots = tuple(root.resolve() for root in roots)
    if not _is_within(resolved, resolved_roots):
        raise PathPolicyError("Path is outside the permitted project area")
    return resolved


def _create_batch_trace_report(context_path: Path, input_path: Path, session_path: Path) -> Path:
    output_path = _resolve_path(
        "",
        default=Path("data/output") / f"report_{session_path.stem}.json",
        access="write",
    )
    evidence_log_path = _resolve_path(
        "",
        default=Path("evidence/evidence_log.csv"),
        access="write",
    )
    run(
        context_path=context_path,
        input_path=input_path,
        output_path=output_path,
        evidence_log_path=evidence_log_path,
    )
    return output_path


def _log_event(event: str, request_id: str, **fields: Any) -> None:
    record = {"event": event, "request_id": request_id, **fields}
    LOGGER.info(json.dumps(record, separators=(",", ":"), sort_keys=True))


def _parse_bool(value: Any, *, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes"}:
            return True
        if normalized in {"false", "0", "no"}:
            return False
    raise RequestValidationError("Boolean fields must be true or false")


def _export_output_path(payload: Dict[str, Any], session_path: Path, suffix: str) -> Path:
    output = str(payload.get("output", "")).strip()
    if output:
        return _resolve_path(output, access="write")
    return _resolve_path(
        "",
        default=Path("evidence/capa_exports") / f"{session_path.stem}-{suffix}.csv",
        access="write",
    )


def _export_target_path(payload: Dict[str, Any], session_path: Path, kind: str) -> Path:
    output = str(payload.get("output", "")).strip()
    if output:
        return _resolve_path(output, access="write")
    if kind == "report":
        return _resolve_path("", default=_default_report_path(session_path), access="write")
    suffix = "capa" if kind == "capa" else "testcases"
    return _export_output_path(payload, session_path, suffix)


def _validated_choice(payload: Dict[str, Any], field: str, default: str, choices: set[str]) -> str:
    value = str(payload.get(field, default)).strip().lower() or default
    if value not in choices:
        allowed = ", ".join(sorted(choices))
        raise RequestValidationError(f"{field} must be one of: {allowed}")
    return value


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: Dict[str, Any]) -> None:
    handler.response_status = status
    body = json.dumps({**payload, "request_id": handler.request_id}, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("X-Request-ID", handler.request_id)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _preview_expiry() -> tuple[float, str]:
    expires_at = time.time() + EXPORT_PREVIEW_TTL_SECONDS
    return expires_at, datetime.fromtimestamp(expires_at, timezone.utc).isoformat()


def _export_binding(payload: Dict[str, Any], kind: str, session_path: Path, target_path: Path) -> str:
    options = {
        key: payload.get(key)
        for key in ("provider", "assignee", "due_date", "assigned_to", "area_path", "iteration_path", "state", "variant_set")
        if key in payload
    }
    binding = {
        "kind": kind,
        "session": str(session_path),
        "target": str(target_path),
        "options": options,
    }
    return hashlib.sha256(json.dumps(binding, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _render_export(payload: Dict[str, Any]) -> tuple[str, Path, str, str]:
    kind = str(payload.get("kind", "")).strip().lower()
    if kind not in {"report", "capa", "ado"}:
        raise RequestValidationError("kind must be one of: report, capa, ado")
    session_path = _resolve_path(str(payload.get("session", "")), access="read")
    target_path = _export_target_path(payload, session_path, kind)

    if kind == "report":
        content = render_report_markdown(session_path=session_path)
    elif kind == "capa":
        content = render_capa_csv(
            session_path=session_path,
            provider=_validated_choice(payload, "provider", "ado", CAPA_PROVIDERS),
            assignee=str(payload.get("assignee", "")),
            due_date=str(payload.get("due_date", "")),
        )
    else:
        content = render_ado_testcases_csv(
            session_path=session_path,
            assigned_to=str(payload.get("assigned_to", "")),
            area_path=str(payload.get("area_path", "")),
            iteration_path=str(payload.get("iteration_path", "")),
            state=str(payload.get("state", "Design")).strip() or "Design",
            variant_set=_validated_choice(payload, "variant_set", "standard", ADO_VARIANT_SETS),
        )
    content_bytes = content.encode("utf-8")
    content_sha256 = hashlib.sha256(content_bytes).hexdigest()
    return kind, target_path, content, content_sha256


def _create_export_preview(payload: Dict[str, Any]) -> Dict[str, Any]:
    kind, target_path, content, content_sha256 = _render_export(payload)
    preview_id = uuid.uuid4().hex
    expires_epoch, expires_at = _preview_expiry()
    session_path = _resolve_path(str(payload.get("session", "")), access="read")
    source_sha256 = hashlib.sha256(session_path.read_bytes()).hexdigest()
    binding_sha256 = _export_binding(payload, kind, session_path, target_path)
    record = {
        "kind": kind,
        "session_path": session_path,
        "source_sha256": source_sha256,
        "target_path": target_path,
        "content": content,
        "content_sha256": content_sha256,
        "binding_sha256": binding_sha256,
        "expires_epoch": expires_epoch,
        "expires_at": expires_at,
    }
    with _EXPORT_PREVIEWS_LOCK:
        _EXPORT_PREVIEWS[preview_id] = record
    return {
        "preview_id": preview_id,
        "target_path": _rel(target_path),
        "exists": target_path.exists(),
        "content_sha256": content_sha256,
        "binding_sha256": binding_sha256,
        "byte_count": len(content.encode("utf-8")),
        "content": content,
        "expires_at": expires_at,
    }


def _commit_export(payload: Dict[str, Any]) -> Dict[str, Any]:
    preview_id = str(payload.get("preview_id", "")).strip()
    if not preview_id:
        raise RequestValidationError("preview_id is required")
    if not _parse_bool(payload.get("approved"), default=False):
        raise RequestValidationError("approved must be true")
    supplied_hash = str(payload.get("content_sha256", "")).strip().lower()
    if not supplied_hash:
        raise RequestValidationError("content_sha256 is required")

    with _EXPORT_PREVIEWS_LOCK:
        record = _EXPORT_PREVIEWS.get(preview_id)
    if record is None or record["expires_epoch"] <= time.time():
        raise ExportConflictError("Export preview is missing or expired")
    if supplied_hash != record["content_sha256"]:
        raise ExportConflictError("Export preview content hash does not match")
    try:
        current_source_sha256 = hashlib.sha256(record["session_path"].read_bytes()).hexdigest()
    except OSError as exc:
        raise ExportConflictError("Export preview source session is no longer available") from exc
    if current_source_sha256 != record["source_sha256"]:
        raise ExportConflictError("Export preview source session has changed")
    supplied_binding = str(payload.get("binding_sha256", "")).strip().lower()
    if supplied_binding and supplied_binding != record["binding_sha256"]:
        raise ExportConflictError("Export preview payload binding does not match")
    binding_fields = {"kind", "session", "output", "provider", "assignee", "due_date", "assigned_to", "area_path", "iteration_path", "state", "variant_set"}
    if binding_fields.intersection(payload):
        try:
            kind, target_path, content, content_sha256 = _render_export(payload)
            session_path = _resolve_path(str(payload.get("session", "")), access="read")
        except (PathPolicyError, RequestValidationError, FileNotFoundError) as exc:
            raise ExportConflictError("Export preview payload has changed") from exc
        binding_sha256 = _export_binding(payload, kind, session_path, target_path)
        if content_sha256 != record["content_sha256"] or binding_sha256 != record["binding_sha256"]:
            raise ExportConflictError("Export preview payload has changed")

    target_path: Path = record["target_path"]
    overwrite = _parse_bool(payload.get("overwrite"), default=False)
    if target_path.exists() and not overwrite:
        raise ExportConflictError("Target already exists; explicit overwrite=true is required")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=target_path.parent, prefix=f".{target_path.name}.", delete=False
        ) as handle:
            temporary_path = handle.name
            handle.write(record["content"])
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, target_path)
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.unlink(temporary_path)

    with _EXPORT_PREVIEWS_LOCK:
        _EXPORT_PREVIEWS.pop(preview_id, None)
    return {"committed_path": _rel(target_path)}


def _serve_preview(handler: BaseHTTPRequestHandler, file_path: Path) -> None:
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(file_path)

    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = file_path.read_bytes().decode("utf-8", errors="replace")

    safe_text = html.escape(text)
    title = file_path.name
    body = (
        "<!doctype html>"
        "<html><head>"
        "<meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        "<style>"
        "body { font-family: Segoe UI, sans-serif; margin: 24px; background: #f8fafc; color: #0f172a; }"
        "pre { background: #fff; border: 1px solid #dbe2ea; border-radius: 10px; padding: 16px; white-space: pre-wrap; word-break: break-word; overflow-wrap: anywhere; }"
        "h1 { font-size: 20px; margin-bottom: 12px; }"
        "</style>"
        "</head><body>"
        f"<h1>{html.escape(title)}</h1>"
        f"<pre>{safe_text}</pre>"
        "</body></html>"
    ).encode("utf-8")

    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _read_json_body(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    content_type = handler.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    if content_type != "application/json":
        raise RequestBodyError("Content-Type must be application/json")
    try:
        size = int(handler.headers.get("Content-Length", "0"))
    except ValueError as exc:
        raise RequestBodyError("Content-Length must be an integer") from exc
    if size < 0 or size > MAX_REQUEST_BODY_BYTES:
        raise RequestBodyError("Request body is too large")
    raw = handler.rfile.read(size) if size > 0 else b"{}"
    if not raw:
        return {}
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RequestBodyError("Request body must contain valid JSON") from exc
    if not isinstance(payload, dict):
        raise RequestBodyError("JSON body must be an object")
    return payload


def _list_context_files() -> List[str]:
    folder = _resolve_path("project-context", access="read")
    if not folder.exists():
        return []
    files = [item for item in folder.glob("*.yaml") if item.is_file()]
    return sorted(_rel(item) for item in files)


def _list_input_files() -> List[str]:
    folder = _resolve_path("data/input", access="read")
    if not folder.exists():
        return []
    files = [item for item in folder.glob("*.json") if item.is_file()]
    valid: List[str] = []
    for item in files:
        try:
            payload = load_json(item)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(payload, list):
            continue
        has_defects = any(isinstance(entry, dict) and str(entry.get("defect_id", "")).strip() for entry in payload)
        if has_defects:
            valid.append(_rel(item))
    return sorted(valid)


def _list_quick_plans() -> List[str]:
    folder = _resolve_path("data/input", access="read")
    if not folder.exists():
        return []
    files = [item for item in folder.glob("*quick_plan*.json") if item.is_file()]
    return sorted(_rel(item) for item in files)


def _list_sessions() -> List[str]:
    folder = _resolve_path("evidence/rca_sessions", access="read")
    if not folder.exists():
        return []
    files = [item for item in folder.glob("*.json") if item.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [_rel(item) for item in files]


def _list_output_reports() -> List[str]:
    folder = _resolve_path("data/output", access="read")
    if not folder.exists():
        return []
    files = [item for item in folder.glob("*.json") if item.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [_rel(item) for item in files]


def _extract_agent_trace(payload: Dict[str, Any], defect_id: str = "") -> Dict[str, Any]:
    analysis = payload.get("analysis", [])
    if not isinstance(analysis, list):
        analysis = []

    entries = [item for item in analysis if isinstance(item, dict)]
    defect_ids = [str(item.get("defect_id", "")).strip() for item in entries if str(item.get("defect_id", "")).strip()]

    selected_entry: Dict[str, Any] | None = None
    normalized = defect_id.strip().lower()
    if normalized:
        for item in entries:
            candidate = str(item.get("defect_id", "")).strip().lower()
            if candidate == normalized:
                selected_entry = item
                break

    if selected_entry is None and entries:
        selected_entry = entries[0]

    if selected_entry is None:
        return {
            "defect_ids": [],
            "selected_defect_id": "",
            "agent_trace": [],
        }

    trace = selected_entry.get("agent_trace", [])
    if not isinstance(trace, list):
        trace = []

    return {
        "defect_ids": defect_ids,
        "selected_defect_id": str(selected_entry.get("defect_id", "")).strip(),
        "agent_trace": trace,
    }


def _list_defect_ids(input_path: Path) -> List[str]:
    payload = load_json(input_path)
    if not isinstance(payload, list):
        return []
    output: List[str] = []
    for defect in payload:
        if isinstance(defect, dict):
            defect_id = str(defect.get("defect_id", "")).strip()
            if defect_id:
                output.append(defect_id)
    return output


class RcaWebHandler(BaseHTTPRequestHandler):
    server_version = "AgenticQAWeb/1.0"

    def _begin_request(self) -> None:
        self.request_id = uuid.uuid4().hex
        self.response_status = HTTPStatus.OK
        _log_event("request.start", self.request_id, method=self.command, endpoint=urlparse(self.path).path)

    def _finish_request(self) -> None:
        _log_event("request.end", self.request_id, method=self.command, status=int(self.response_status))

    def _handle_exception(self, exc: Exception) -> None:
        if isinstance(exc, ExportConflictError):
            status = HTTPStatus.CONFLICT
            error_code = "EXPORT_CONFLICT"
            message = str(exc)
        elif isinstance(exc, (PathPolicyError, RequestValidationError, RequestBodyError, json.JSONDecodeError)):
            status = HTTPStatus.BAD_REQUEST
            error_code = "INVALID_REQUEST" if not isinstance(exc, PathPolicyError) else "PATH_NOT_ALLOWED"
            message = str(exc)
        elif isinstance(exc, (FileNotFoundError, IsADirectoryError)):
            status = HTTPStatus.NOT_FOUND
            error_code = "RESOURCE_NOT_FOUND"
            message = "Requested resource was not found"
        else:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
            error_code = "INTERNAL_ERROR"
            message = "Internal server error"
        error_fields: Dict[str, Any] = {"error_code": error_code}
        if status >= HTTPStatus.INTERNAL_SERVER_ERROR:
            error_fields.update(
                exception=type(exc).__name__,
                traceback=traceback.format_exc(),
            )
        _log_event("request.error", self.request_id, **error_fields)
        self.response_status = status
        _json_response(
            self,
            status,
            {"error_code": error_code, "message": message, "error": message},
        )

    def do_GET(self) -> None:  # noqa: N802
        self._begin_request()
        try:
            self._dispatch_get()
        except Exception as exc:  # noqa: BLE001
            self._handle_exception(exc)
        finally:
            self._finish_request()

    def _dispatch_get(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/api/health":
            _json_response(self, HTTPStatus.OK, {"status": "ok"})
            return

        if parsed.path == "/api/bootstrap":
            _json_response(
                self,
                HTTPStatus.OK,
                {
                    "project_root": _rel(PROJECT_ROOT),
                    "contexts": _list_context_files(),
                    "inputs": _list_input_files(),
                    "quick_plans": _list_quick_plans(),
                    "sessions": _list_sessions(),
                    "output_reports": _list_output_reports(),
                },
            )
            return

        if parsed.path == "/api/file-preview":
            query = parse_qs(parsed.query)
            file_value = (query.get("path") or [""])[0]
            if not file_value:
                raise RequestValidationError("Missing query parameter: path")
            preview_path = _resolve_path(file_value, access="read")
            _serve_preview(self, preview_path)
            return

        if parsed.path == "/api/defects":
            query = parse_qs(parsed.query)
            input_value = (query.get("input") or [""])[0]
            if not input_value:
                raise RequestValidationError("Missing query parameter: input")
            input_path = _resolve_path(input_value, access="read")
            defect_ids = _list_defect_ids(input_path)
            _json_response(self, HTTPStatus.OK, {"defect_ids": defect_ids})
            return

        if parsed.path == "/api/report-agent-trace":
            query = parse_qs(parsed.query)
            report_value = (query.get("report") or [""])[0]
            defect_value = (query.get("defect_id") or [""])[0]
            if not report_value:
                raise RequestValidationError("Missing query parameter: report")
            report_path = _resolve_path(report_value, access="read")
            payload = load_json(report_path)
            if not isinstance(payload, dict):
                raise RequestValidationError("Report JSON must be an object")
            trace_payload = _extract_agent_trace(payload, defect_id=defect_value)
            _json_response(
                self,
                HTTPStatus.OK,
                {
                    "report": _rel(report_path),
                    **trace_payload,
                },
            )
            return

        if parsed.path == "/" or parsed.path == "/index.html":
            self._serve_file(WEB_ROOT / "index.html", "text/html; charset=utf-8")
            return

        raise FileNotFoundError(parsed.path)

    def do_POST(self) -> None:  # noqa: N802
        self._begin_request()
        try:
            self._dispatch_post()
        except Exception as exc:  # noqa: BLE001
            self._handle_exception(exc)
        finally:
            self._finish_request()

    def _dispatch_post(self) -> None:
        parsed = urlparse(self.path)
        payload = _read_json_body(self)

        if parsed.path == "/api/start":
            self._handle_start(payload)
            return
        if parsed.path == "/api/answer":
            self._handle_answer(payload)
            return
        if parsed.path == "/api/status":
            self._handle_status(payload)
            return
        if parsed.path == "/api/export-preview":
            self._handle_export_preview(payload)
            return
        if parsed.path == "/api/export-commit":
            self._handle_export_commit(payload)
            return
        if parsed.path == "/api/export-report":
            self._handle_export_report(payload)
            return
        if parsed.path == "/api/export-capa":
            self._handle_export_capa(payload)
            return
        if parsed.path == "/api/export-ado-testcases":
            self._handle_export_ado_testcases(payload)
            return
        if parsed.path == "/api/run-quick-plan":
            self._handle_run_quick_plan(payload)
            return
        if parsed.path == "/api/run-demo":
            self._handle_run_demo(payload)
            return

        raise FileNotFoundError(parsed.path)

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def _serve_file(self, path: Path, content_type: str) -> None:
        path = _resolve_path(str(path), access="read")
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(path)
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_start(self, payload: Dict[str, Any]) -> None:
        context_path = _resolve_path(str(payload.get("context", "")), access="read")
        input_path = _resolve_path(str(payload.get("input", "")), access="read")
        defect_id = str(payload.get("defect_id", "")).strip()
        if not defect_id:
            raise RequestValidationError("defect_id is required")

        session_hint = str(payload.get("session", "")).strip()
        if session_hint:
            session_path = _resolve_path(session_hint, access="write")
        else:
            session_path = _resolve_path("", default=_default_session_path(defect_id), access="write")

        context, quality_gates = _load_context_bundle(context_path)
        session = start_session(
            context=context,
            quality_gates=quality_gates,
            input_path=input_path,
            defect_id=defect_id,
            session_path=session_path,
        )

        suggestions = _discover_evidence_refs(PROJECT_ROOT, session)
        batch_report_path = _create_batch_trace_report(context_path, input_path, session_path)
        _json_response(
            self,
            HTTPStatus.OK,
            {
                "session_path": _rel(session_path),
                "session": session,
                "evidence_suggestions": suggestions,
                "default_report_path": _rel(_resolve_path("", default=_default_report_path(session_path), access="write")),
                "batch_report_path": _rel(batch_report_path),
            },
        )

    def _handle_answer(self, payload: Dict[str, Any]) -> None:
        session_path = _resolve_path(str(payload.get("session", "")), access="read")
        answer = str(payload.get("answer", "")).strip()
        if not answer:
            raise RequestValidationError("answer is required")

        refs_value = payload.get("evidence_refs", [])
        if not isinstance(refs_value, list):
            raise RequestValidationError("evidence_refs must be a list")
        evidence_refs = [str(item).strip() for item in refs_value if str(item).strip()]

        resolved = _parse_bool(payload.get("resolved"), default=False)
        controllable = _parse_bool(payload.get("controllable"), default=True)
        prevents_recurrence = _parse_bool(payload.get("prevents_recurrence"), default=False)
        revise = _parse_bool(payload.get("revise"), default=False)
        advanced_continuation = _parse_bool(payload.get("advanced_continuation"), default=False)
        target_why_index = payload.get("target_why_index")
        if target_why_index is not None:
            try:
                target_why_index = int(target_why_index)
            except (TypeError, ValueError) as exc:
                raise RequestValidationError("target_why_index must be an integer") from exc
            if target_why_index < 1:
                raise RequestValidationError("target_why_index must be positive")

        if revise:
            session = revise_current_answer(
                session_path=session_path,
                answer=answer,
                evidence_refs=evidence_refs,
                resolved=resolved,
                controllable=controllable,
                prevents_recurrence=prevents_recurrence,
                target_why_index=target_why_index,
            )
        else:
            session = answer_session(
                session_path=session_path,
                answer=answer,
                evidence_refs=evidence_refs,
                resolved=resolved,
                controllable=controllable,
                prevents_recurrence=prevents_recurrence,
                advanced_continuation=advanced_continuation,
            )

        suggestions = _discover_evidence_refs(PROJECT_ROOT, session)
        _json_response(
            self,
            HTTPStatus.OK,
            {
                "session_path": _rel(session_path),
                "session": session,
                "evidence_suggestions": suggestions,
            },
        )

    def _handle_status(self, payload: Dict[str, Any]) -> None:
        session_path = _resolve_path(str(payload.get("session", "")), access="read")
        session = load_session_status(session_path)
        suggestions = _discover_evidence_refs(PROJECT_ROOT, session)
        _json_response(
            self,
            HTTPStatus.OK,
            {
                "session_path": _rel(session_path),
                "session": session,
                "evidence_suggestions": suggestions,
            },
        )

    def _handle_export_preview(self, payload: Dict[str, Any]) -> None:
        _json_response(self, HTTPStatus.OK, _create_export_preview(payload))

    def _handle_export_commit(self, payload: Dict[str, Any]) -> None:
        _json_response(self, HTTPStatus.OK, _commit_export(payload))

    def _handle_export_report(self, payload: Dict[str, Any]) -> None:
        preview = _create_export_preview({**payload, "kind": "report"})
        committed = _commit_export(
            {
                "preview_id": preview["preview_id"],
                "approved": True,
                "content_sha256": preview["content_sha256"],
                "overwrite": payload.get("overwrite", False),
            }
        )
        _json_response(self, HTTPStatus.OK, {"report_path": committed["committed_path"]})

    def _handle_export_capa(self, payload: Dict[str, Any]) -> None:
        preview = _create_export_preview({**payload, "kind": "capa"})
        committed = _commit_export(
            {
                "preview_id": preview["preview_id"],
                "approved": True,
                "content_sha256": preview["content_sha256"],
                "overwrite": payload.get("overwrite", False),
            }
        )
        provider = _validated_choice(payload, "provider", "ado", CAPA_PROVIDERS)
        _json_response(self, HTTPStatus.OK, {"csv_path": committed["committed_path"], "provider": provider})

    def _handle_export_ado_testcases(self, payload: Dict[str, Any]) -> None:
        preview = _create_export_preview({**payload, "kind": "ado"})
        committed = _commit_export(
            {
                "preview_id": preview["preview_id"],
                "approved": True,
                "content_sha256": preview["content_sha256"],
                "overwrite": payload.get("overwrite", False),
            }
        )
        variant_set = _validated_choice(payload, "variant_set", "standard", ADO_VARIANT_SETS)
        _json_response(
            self,
            HTTPStatus.OK,
            {"csv_path": committed["committed_path"], "schema": "ado-testcase", "variant_set": variant_set},
        )

    def _handle_run_quick_plan(self, payload: Dict[str, Any]) -> None:
        context_path = _resolve_path(str(payload.get("context", "")), access="read")
        input_path = _resolve_path(str(payload.get("input", "")), access="read")
        defect_id = str(payload.get("defect_id", "")).strip()
        if not defect_id:
            raise RequestValidationError("defect_id is required")

        quick_plan_path = _resolve_path(str(payload.get("quick_plan", "")), access="read")
        quick_plan = _load_quick_plan(quick_plan_path)
        role = str(payload.get("role", "qa"))

        session_hint = str(payload.get("session", "")).strip()
        if session_hint:
            session_path = _resolve_path(session_hint, access="write")
        else:
            session_path = _resolve_path("", default=_default_session_path(defect_id), access="write")

        output_hint = str(payload.get("output_report", "")).strip()
        if output_hint:
            output_report_path = _resolve_path(output_hint, access="write")
        else:
            output_report_path = _resolve_path("", default=_default_report_path(session_path), access="write")

        result = run_guided_rca(
            context_path=context_path,
            input_path=input_path,
            defect_id=defect_id,
            session_path=session_path,
            role=role,
            output_report_path=output_report_path,
            quick_plan=quick_plan,
        )
        session = load_session_status(session_path)
        suggestions = _discover_evidence_refs(PROJECT_ROOT, session)
        batch_report_path = _create_batch_trace_report(context_path, input_path, session_path)
        _json_response(
            self,
            HTTPStatus.OK,
            {
                "result": result,
                "session_path": _rel(session_path),
                "session": session,
                "evidence_suggestions": suggestions,
                "report_path": _rel(output_report_path),
                "batch_report_path": _rel(batch_report_path),
            },
        )

    def _handle_run_demo(self, payload: Dict[str, Any]) -> None:
        context_path = _resolve_path(str(payload.get("context", "project-context/baseline-project.yaml")), access="read")
        input_path = _resolve_path(str(payload.get("input", "data/input/demo_cases.json")), access="read")
        case_name = str(payload.get("case", "why3"))
        role = str(payload.get("role", "qa"))

        session_hint = str(payload.get("session", "")).strip()
        session_path = _resolve_path(session_hint, access="write") if session_hint else None
        output_hint = str(payload.get("output_report", "")).strip()
        output_report_path = _resolve_path(output_hint, access="write") if output_hint else None

        result = run_demo(
            case_name=case_name,
            context_path=context_path,
            input_path=input_path,
            session_path=session_path,
            output_report_path=output_report_path,
            role=role,
        )
        active_session_path = _resolve_path(result["session_path"], access="read")
        session = load_session_status(active_session_path)
        suggestions = _discover_evidence_refs(PROJECT_ROOT, session)
        _json_response(
            self,
            HTTPStatus.OK,
            {
                "result": result,
                "session_path": _rel(active_session_path),
                "session": session,
                "evidence_suggestions": suggestions,
                "report_path": _rel(_resolve_path(result["report_path"], access="read")),
                "capa_path": _rel(_resolve_path(result["capa_path"], access="read")),
                "testcases_path": _rel(_resolve_path(result["testcases_path"], access="read")),
                "batch_report_path": _rel(_resolve_path(result["batch_report_path"], access="read")),
            },
        )


def run_server(host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), RcaWebHandler)
    print(f"Agentic QA Web UI running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agentic QA RCA local web UI")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface. Default 127.0.0.1")
    parser.add_argument("--port", type=int, default=8787, help="Port number. Default 8787")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
