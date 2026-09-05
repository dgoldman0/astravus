#!/usr/bin/env python3
"""Local Ren'Py workflow. Downloads, state, and exports stay inside ignored folders."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
CACHE = PROJECT / ".cache"
VERSION = "8.5.3"
SDK = Path(os.environ.get("ASTRAVUS_RENPY_SDK", CACHE / f"renpy-{VERSION}-sdk")).resolve()
CHECKSUMS = {
    f"renpy-{VERSION}-sdk.tar.bz2": "eb0a9be7f0fb13632fe25ceade9a8bed5a1b4d6b6e83bd19eeeb29e1a1bb4a45",
    f"renpy-{VERSION}-web.zip": "954db897e65f51ea63cb2fb7b203d02be0447f4e22069514020bbe6c6691fdfc",
}
RELEASE_VERSION = r"\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*)?"


def download(name):
    CACHE.mkdir(parents=True, exist_ok=True)
    archive = CACHE / name
    if not archive.exists():
        url = f"https://www.renpy.org/dl/{VERSION}/{name}"
        print(f"Downloading {url}", flush=True)
        partial = archive.with_suffix(archive.suffix + ".part")
        with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as out:
            shutil.copyfileobj(response, out)
        partial.replace(archive)
    with archive.open("rb") as data:
        actual = hashlib.file_digest(data, "sha256").hexdigest()
    if actual != CHECKSUMS[name]:
        raise SystemExit(f"Checksum mismatch: {archive}. Remove this cached download and try again.")
    return archive


def install():
    if os.environ.get("ASTRAVUS_RENPY_SDK"):
        raise SystemExit("Unset ASTRAVUS_RENPY_SDK to install the pinned SDK into .cache.")
    archive = download(f"renpy-{VERSION}-sdk.tar.bz2")
    if not (SDK / "renpy.py").exists():
        with tarfile.open(archive) as source:
            source.extractall(CACHE, filter="data")
    archive = download(f"renpy-{VERSION}-web.zip")
    if not (SDK / "web" / "index.html").exists():
        with zipfile.ZipFile(archive) as source:
            for name in source.namelist():
                if not (SDK / name).resolve().is_relative_to(SDK):
                    raise SystemExit(f"Unsafe archive path: {name}")
            source.extractall(SDK)
    print(f"Ready: {SDK}")


def engine(*args, headless=False, testing=False):
    if not (SDK / "renpy.py").exists():
        raise SystemExit("SDK missing. Run: python3 scripts/project.py install")
    if sys.platform == "win32":
        command = [str(SDK / "lib/py3-windows-x86_64/python.exe"), str(SDK / "renpy.py")]
    else:
        command = [str(SDK / "renpy.sh")]
    command.extend(map(str, args))
    state = PROJECT / ("test-results/state" if testing else ".cache/state")
    state.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, RENPY_PATH_TO_SAVES=str(state))
    if headless:
        if not shutil.which("xvfb-run"):
            raise SystemExit("Headless tests require xvfb-run. Otherwise run test in a desktop session.")
        command = ["xvfb-run", "-a", "-s", "-screen 0 1920x1080x24", *command]
        env["SDL_AUDIODRIVER"] = "dummy"
    subprocess.run(command, cwd=PROJECT, env=env, check=True)


def prepare_web():
    """Install browser startup/cache fixes without modifying the downloaded SDK."""
    web = PROJECT / "build/web"
    index = web / "index.html"
    html = index.read_text()
    original = '<script src="renpy-pre.js"></script>\n  <script async type="text/javascript" src="renpy.js"></script>'
    if original not in html:
        raise SystemExit("Unexpected Ren'Py web template: startup guard was not installed.")
    # Version game data and bootstrap URLs even if an older worker still owns
    # the first navigation. Saves live separately in IndexedDB.
    digest = hashlib.sha256((web / "game.zip").read_bytes())
    for name in ("startup.js", "service-worker.js"):
        source = PROJECT / "web" / name
        digest.update(source.read_bytes())
        shutil.copyfile(source, web / name)
    build_id = digest.hexdigest()[:16]
    worker_registration = """      // Register the service worker.
      if (navigator.serviceWorker) {
          if (!navigator.serviceWorker.controller) {
              navigator.serviceWorker.register('./service-worker.js', { updateViaCache: 'all' });
          }
      }"""
    if worker_registration not in html or "window.gameZipURL = 'game.zip';" not in html:
        raise SystemExit("Unexpected Ren'Py web template: cache fixes were not installed.")
    html = html.replace(worker_registration, "      // startup.js updates the worker before starting the engine.")
    html = html.replace("window.gameZipURL = 'game.zip';", f"window.gameZipURL = 'game.zip?build={build_id}';")
    html = html.replace(original, f'<script src="startup.js?build={build_id}"></script>')
    index.write_text(html)
    catalog_path = web / "pwa_catalog.json"
    catalog = json.loads(catalog_path.read_text())
    catalog["files"] = [f"game.zip?build={build_id}" if name == "game.zip" else name for name in catalog["files"]]
    catalog["files"].append(f"startup.js?build={build_id}")
    catalog_path.write_text(json.dumps(catalog))
    with zipfile.ZipFile(PROJECT / "build/web.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(web.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(web).as_posix())


def prune_desktop_exports():
    """Keep the current release after both ZIPs pass CRC checks, including resets."""
    options = (PROJECT / "game/options.rpy").read_text()
    version_match = re.search(rf'^define config.version = "({RELEASE_VERSION})"$', options, re.M)
    if version_match is None:
        raise SystemExit("Unsupported release version. Existing exports retained.")
    version = version_match.group(1)
    name = re.search(r'^define build.name = "([\w-]+)"$', options, re.M).group(1)
    dist = PROJECT / "dist"
    current = {dist / f"{name}-{version}-{platform}.zip" for platform in ("pc", "mac")}
    for platform in ("pc", "mac"):
        path = dist / f"{name}-{version}-{platform}.zip"
        with zipfile.ZipFile(path) as archive:
            if not any(not member.is_dir() for member in archive.infolist()):
                raise SystemExit(f"Empty export: {path}. Existing exports retained.")
            bad_member = archive.testzip()
            if bad_member:
                raise SystemExit(f"Corrupt export: {path}: {bad_member}. Existing exports retained.")
    removed_bytes = 0
    for path in dist.glob("*.zip"):
        match = re.fullmatch(rf"astravus-(?:book|chapter)-one-{RELEASE_VERSION}-(?:pc|mac)\.zip", path.name)
        # Version numbers may deliberately restart (0.2.7 -> 0.1-alpha).
        # Only this project's recognized exports are replaced; unrelated ZIPs
        # and save directories never participate in retention.
        if match and path not in current:
            removed_bytes += path.stat().st_size
            path.unlink()
    print(f"Desktop exports checked; removed {removed_bytes / 1024**2:.1f} MiB of superseded builds.")


def content_review_gate(review_build):
    if review_build:
        print("Review build: final content approval is bypassed for testing; this is not a release candidate.", flush=True)
        return
    subprocess.run([sys.executable, PROJECT / "scripts/release_review.py", "status",
                    "--phase", "content", "--strict"], cwd=PROJECT, check=True)


def record_build(kind, review_build):
    options = (PROJECT / "game/options.rpy").read_text()
    version = re.search(r'^define config.version = "([^"]+)"$', options, re.M).group(1)
    name = re.search(r'^define build.name = "([^"]+)"$', options, re.M).group(1)
    files = ([PROJECT / "dist" / f"{name}-{version}-{platform}.zip" for platform in ("pc", "mac")]
             if kind == "desktop" else [PROJECT / "build/web.zip"])
    stamp = PROJECT / "build/release-builds.json"
    record = {"kind": "review" if review_build else "candidate", "version": version,
              "built_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "files": {}}
    for path in files:
        with path.open("rb") as stream:
            record["files"][path.relative_to(PROJECT).as_posix()] = hashlib.file_digest(stream, "sha256").hexdigest()
    stamp.parent.mkdir(parents=True, exist_ok=True)
    with stamp.with_suffix(".lock").open("w") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        data = json.loads(stamp.read_text()) if stamp.exists() else {"schema_version": 1, "builds": {}}
        data["builds"][kind] = record
        temporary = stamp.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2) + "\n")
        temporary.replace(stamp)


class PreviewRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Local previews must re-read rebuilt files instead of caching them."""

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("install", "run", "lint"):
        commands.add_parser(name)
    for name in ("build", "web"):
        build = commands.add_parser(name)
        build.add_argument("--review-build", action="store_true",
                           help="Build temporary test artifacts before content approval; excluded from final release signoff")
    test = commands.add_parser("test")
    test.add_argument("--headless", action="store_true")
    test.add_argument("--suite", choices=("chapter_playthrough", "closing_theme_review", "character_framing_review", "glossary_review", "environment_grounding_review", "environment_state_review"),
                      default="chapter_playthrough")
    review = commands.add_parser("review", help="Show the current release acceptance matrix")
    review.add_argument("--phase", choices=("content", "runtime", "exports"), default="exports")
    review.add_argument("--strict", action="store_true")
    serve = commands.add_parser("serve")
    serve.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.command == "install":
        install()
    elif args.command == "run":
        engine(PROJECT)
    elif args.command == "lint":
        engine(PROJECT, "lint")
    elif args.command == "review":
        command = [sys.executable, PROJECT / "scripts/release_review.py", "status", "--phase", args.phase]
        if args.strict:
            command.append("--strict")
        subprocess.run(command, cwd=PROJECT, check=True)
    elif args.command == "test":
        engine(PROJECT, "test", args.suite, "--overwrite-screenshots",
               "--hide-execution", "hooks", headless=args.headless, testing=True)
        if args.suite == "character_framing_review":
            subprocess.run([sys.executable, PROJECT / "scripts/character_layout.py", "--renders",
                            PROJECT / "test-results/character-layout"], cwd=PROJECT, check=True)
    elif args.command == "build":
        if not args.review_build:
            subprocess.run([sys.executable, PROJECT / "scripts/check_assets.py"], cwd=PROJECT, check=True)
        content_review_gate(args.review_build)
        engine(SDK / "launcher", "distribute", PROJECT, "--destination", PROJECT / "dist",
               "--package", "pc", "--package", "mac")
        prune_desktop_exports()
        record_build("desktop", args.review_build)
    elif args.command == "web":
        if not args.review_build:
            subprocess.run([sys.executable, PROJECT / "scripts/check_assets.py"], cwd=PROJECT, check=True)
        content_review_gate(args.review_build)
        if not (SDK / "web").is_dir():
            raise SystemExit("Web support missing. Run: python3 scripts/project.py install")
        engine(SDK / "launcher", "web_build", PROJECT, "--destination", PROJECT / "build/web")
        prepare_web()
        record_build("web", args.review_build)
    elif args.command == "serve":
        web = PROJECT / "build/web"
        if not (web / "index.html").exists():
            raise SystemExit("Build the browser version first: python3 scripts/project.py web")
        handler = functools.partial(PreviewRequestHandler, directory=str(web))
        with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
            print(f"Open http://127.0.0.1:{args.port} — Ctrl+C to stop.", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
