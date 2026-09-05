#!/usr/bin/env python3
"""Verify delivered desktop/browser archives against the final runtime source tree."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import re
import zipfile
import zlib

PROJECT = Path(__file__).resolve().parents[1]
EXCLUDED = ("scripts/", "tests/", "docs/", "web/", "build/", "dist/", "test-results/",
            "marketing/", ".cache/", ".git/", "game/cache/", "game/saves/",
            "game/testcases.rpy", "game/glossary_testcases.rpy")
EXTENSIONS = {".rpy", ".py", ".json", ".png", ".jpg", ".svg", ".ttf", ".otf",
              ".ogg", ".wav", ".mp3", ".md", ".txt"}
# Ren'Py 8.5.3 explicitly includes its Python 3.12 bytecode in 00build.rpy
# and injects build_info.json in distribute.rpy after project classification.
# These are generated runtime files, not the developer image/prediction cache.
GENERATED_RUNTIME = {"game/cache/build_info.json", "game/cache/bytecode-312.rpyb"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check_crc(archive):
    assert archive.namelist(), "Empty ZIP"
    bad = archive.testzip()
    assert bad is None, f"Corrupt ZIP entry: {bad}"


def check_members(archive, prefix=""):
    bad = []
    for member in archive.infolist():
        if not member.filename.startswith(prefix):
            continue
        name = member.filename[len(prefix):]
        if name in GENERATED_RUNTIME or (name == "game/cache/" and member.is_dir()):
            continue
        if any(name.startswith(excluded) for excluded in EXCLUDED):
            bad.append(member.filename)
    assert not bad, f"Development or save files packaged: {bad}"


def check_generated_runtime(archive, prefix, version):
    info = json.loads(archive.read(prefix + "game/cache/build_info.json"))
    assert info.get("version") == version and info.get("name") == "Astravus — Seeds of Youth", info
    assert isinstance(info.get("time"), (int, float)) and info["time"] > 0, info
    bytecode = archive.read(prefix + "game/cache/bytecode-312.rpyb")
    assert zlib.decompress(bytecode), "Empty or damaged Ren'Py runtime bytecode cache"
    return sorted(GENERATED_RUNTIME)


def check_candidate_builds(version):
    stamp = PROJECT / "build/release-builds.json"
    assert stamp.is_file(), "Missing build provenance; rebuild through scripts/project.py"
    builds = json.loads(stamp.read_text())["builds"]
    for kind in ("desktop", "web"):
        build = builds.get(kind, {})
        assert build.get("kind") == "candidate", f"{kind}: review-only or unrecorded build cannot pass final package signoff"
        assert build.get("version") == version, f"{kind}: wrong recorded version"
        assert build.get("files"), f"{kind}: missing artifact identities"
        for name, expected in build["files"].items():
            path = PROJECT / name
            assert path.is_file() and archive_digest(path) == expected, f"Changed candidate artifact: {name}"


def check():
    options = (PROJECT / "game/options.rpy").read_text()
    version = re.search(r'^define config.version = "([^"]+)"$', options, re.M).group(1)
    check_candidate_builds(version)
    base = re.search(r'^define build.name = "([^"]+)"$', options, re.M).group(1)
    files = [path for path in (PROJECT / "game").rglob("*") if path.is_file()
             and path.suffix in EXTENSIONS
             and not any(path.relative_to(PROJECT).as_posix().startswith(prefix) for prefix in EXCLUDED)]
    files.append(PROJECT / "README.md")
    source = {path.relative_to(PROJECT).as_posix(): digest(path.read_bytes()) for path in sorted(files)}
    report = {"version": version, "runtime_files": len(source), "exports": {},
              "limit": "Archive construction and byte integrity only; not Windows/macOS launch verification."}
    for platform in ("pc", "mac"):
        path = PROJECT / "dist" / f"{base}-{version}-{platform}.zip"
        with zipfile.ZipFile(path) as archive:
            check_crc(archive)
            prefix = f"{base}-{version}-pc/" if platform == "pc" else f"{base}.app/Contents/Resources/autorun/"
            check_members(archive, prefix)
            generated = check_generated_runtime(archive, prefix, version)
            for name, expected in source.items():
                assert digest(archive.read(prefix + name)) == expected, (platform, "Changed runtime file", name)
            if platform == "pc":
                assert prefix + base + ".exe" in archive.namelist(), "Missing Windows launcher"
                launcher = archive.getinfo(prefix + base + ".sh")
                assert (launcher.external_attr >> 16) & 0o111, "Linux launcher lacks executable permissions"
            else:
                executables = [member for member in archive.infolist()
                               if member.filename.startswith(f"{base}.app/Contents/MacOS/") and not member.is_dir()]
                assert executables and any((member.external_attr >> 16) & 0o111 for member in executables), "Missing executable macOS launcher"
                assert archive.read("README.md") == (PROJECT / "README.md").read_bytes()
            report["exports"][platform] = {"file": path.relative_to(PROJECT).as_posix(),
                "bytes": path.stat().st_size, "sha256": archive_digest(path),
                "entries": len(archive.namelist()), "matching_runtime_files": len(source),
                "generated_engine_files": generated}
    path = PROJECT / "build/web.zip"
    with zipfile.ZipFile(path) as archive:
        check_crc(archive)
        assert "index.html" in archive.namelist(), "Browser ZIP needs index.html at its root"
        assert archive.read("index.html") == (PROJECT / "build/web/index.html").read_bytes()
        assert archive.read("game.zip") == (PROJECT / "build/web/game.zip").read_bytes()
        with zipfile.ZipFile(io.BytesIO(archive.read("game.zip"))) as game:
            check_crc(game)
            check_members(game)
            generated = check_generated_runtime(game, "", version)
            check_members(archive)
            for name, expected in source.items():
                content = archive.read(name) if name in archive.namelist() else game.read(name)
                assert digest(content) == expected, ("web", "Changed runtime file", name)
            report["exports"]["web"] = {"file": path.relative_to(PROJECT).as_posix(),
                "bytes": path.stat().st_size, "sha256": archive_digest(path),
                "entries": len(archive.namelist()), "game_entries": len(game.namelist()),
                "matching_runtime_files": len(source), "generated_engine_files": generated}
    output = PROJECT / "test-results/release-exports.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    check()
