from __future__ import annotations

import argparse
import importlib
import socket
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "src/main.py",
    "src/web_app.py",
    "web/index.html",
    "project-context/baseline-project.yaml",
    "requirements.txt",
]


def write_check(status: str, message: str) -> None:
    print(f"[{status}] {message}")


def find_available_port(start_port: int, max_attempts: int = 50) -> int:
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    return -1


def check_environment(project_root: Path, port: int) -> int:
    failed = False

    print("Agentic QA RCA Shareable - Environment Check")
    print(f"Project root: {project_root}")
    print()

    major, minor = sys.version_info[:2]
    if major > 3 or (major == 3 and minor >= 10):
        write_check("PASS", f"Python version is compatible: {sys.version.split()[0]}")
    else:
        write_check("FAIL", f"Python 3.10+ required. Detected: {sys.version.split()[0]}")
        failed = True

    try:
        importlib.import_module("yaml")
        write_check("PASS", "PyYAML import check passed.")
    except Exception:
        write_check("FAIL", "PyYAML is not installed. Run: pip install -r requirements.txt")
        failed = True

    for rel in REQUIRED_PATHS:
        target = project_root / rel
        if target.exists():
            write_check("PASS", f"Found: {rel}")
        else:
            write_check("FAIL", f"Missing: {rel}")
            failed = True

    recommended_port = find_available_port(port)
    if recommended_port == -1:
        write_check("FAIL", f"No available port found from {port} to {port + 49}.")
        failed = True
    elif recommended_port != port:
        write_check("WARN", f"Port {port} is in use. Suggested fallback: {recommended_port}")
    else:
        write_check("PASS", f"Port {port} appears available for the web app.")

    print()
    if failed:
        print("Environment check completed with failures. Fix the FAIL items and rerun.")
        return 1

    print("Environment check passed.")
    print(f"Start command: python src/web_app.py --host 127.0.0.1 --port {recommended_port}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-platform environment check for shareable package")
    parser.add_argument("--port", type=int, default=8787, help="Preferred port. Default: 8787")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parent
    return check_environment(project_root, args.port)


if __name__ == "__main__":
    raise SystemExit(main())
