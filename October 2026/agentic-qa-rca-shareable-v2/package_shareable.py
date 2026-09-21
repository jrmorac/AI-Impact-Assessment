from __future__ import annotations

import argparse
import shutil
import tempfile
from datetime import datetime
from pathlib import Path


FOLDERS_TO_REMOVE = {"__pycache__", ".venv", "venv", ".git"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create clean shareable zip package")
    parser.add_argument("--package-name", default="agentic-qa-rca-shareable", help="Package base name")
    parser.add_argument("--output-dir", default="", help="Output directory. Default: sibling dist/")
    return parser.parse_args()


def should_remove_runtime_file(path: Path, staging_root: Path) -> bool:
    rel = path.relative_to(staging_root).as_posix()
    if path.suffix == ".pyc":
        return True
    runtime_prefixes = (
        "data/output/",
        "evidence/rca_sessions/",
        "evidence/rca_reports/",
        "evidence/capa_exports/",
    )
    if rel.startswith(runtime_prefixes):
        return True
    if rel == "evidence/evidence_log.csv":
        return True
    return False


def create_package(source_root: Path, package_name: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = output_dir / f"{package_name}-{timestamp}.zip"

    with tempfile.TemporaryDirectory(prefix=f"{package_name}-{timestamp}-") as tmp:
        staging_root = Path(tmp)
        shutil.copytree(source_root, staging_root, dirs_exist_ok=True)

        for folder in list(staging_root.rglob("*")):
            if folder.is_dir() and folder.name in FOLDERS_TO_REMOVE:
                shutil.rmtree(folder, ignore_errors=True)

        for file_path in list(staging_root.rglob("*")):
            if file_path.is_file() and should_remove_runtime_file(file_path, staging_root):
                file_path.unlink(missing_ok=True)

        if zip_path.exists():
            zip_path.unlink()

        archive_base = zip_path.with_suffix("")
        shutil.make_archive(str(archive_base), "zip", root_dir=staging_root)

    return zip_path


def main() -> int:
    args = parse_args()
    source_root = Path(__file__).resolve().parent
    parent_root = source_root.parent
    output_dir = Path(args.output_dir) if args.output_dir else parent_root / "dist"
    if not output_dir.is_absolute():
        output_dir = (source_root / output_dir).resolve()

    zip_path = create_package(source_root, args.package_name, output_dir)
    print(f"Package created: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
