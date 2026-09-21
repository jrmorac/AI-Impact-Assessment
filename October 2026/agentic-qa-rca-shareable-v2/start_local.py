from __future__ import annotations

import argparse
import socket
import subprocess
import sys
from pathlib import Path


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


def run_check(project_root: Path, port: int) -> int:
    check_script = project_root / "check_env.py"
    cmd = [sys.executable, str(check_script), "--port", str(port)]
    return subprocess.call(cmd, cwd=project_root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-platform launcher for local web UI")
    parser.add_argument("--port", type=int, default=8787, help="Starting port to try. Default: 8787")
    parser.add_argument("--host", default="127.0.0.1", help="Host address. Default: 127.0.0.1")
    parser.add_argument("--skip-check", action="store_true", help="Skip environment check")
    parser.add_argument("--dry-run", action="store_true", help="Show command without starting server")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parent

    if not args.skip_check:
        check_code = run_check(project_root, args.port)
        if check_code != 0:
            print("Environment check failed. Launcher stopped.")
            return check_code

    selected_port = find_available_port(args.port)
    if selected_port == -1:
        print(f"No available port found from {args.port} to {args.port + 49}.")
        return 1

    if selected_port != args.port:
        print(f"Requested port {args.port} is in use. Using {selected_port}.")

    cmd = [sys.executable, "src/web_app.py", "--host", args.host, "--port", str(selected_port)]
    print("Starting local web app...")
    print(" ".join(cmd))

    if args.dry_run:
        print("Dry-run mode enabled. Server was not started.")
        return 0

    return subprocess.call(cmd, cwd=project_root)


if __name__ == "__main__":
    raise SystemExit(main())
