#!/usr/bin/env python3
"""Small dependency-free validator for the EMCR'2028 static website."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.refs: list[tuple[str, int]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if attrs_dict.get("id"):
            self.ids.add(attrs_dict["id"])
        for key in ("href", "src"):
            value = attrs_dict.get(key)
            if value:
                self.refs.append((value, self.getpos()[0]))


def main() -> int:
    if not INDEX.exists():
        print("ERROR: index.html not found")
        return 1

    parser = SiteParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))

    errors: list[str] = []
    external_schemes = {"http", "https", "mailto", "tel", "data"}

    for raw_ref, line in parser.refs:
        ref = raw_ref.strip()
        if not ref or ref == "#":
            continue

        parsed = urlparse(ref)
        if parsed.scheme in external_schemes or ref.startswith("//"):
            continue

        if ref.startswith("#"):
            fragment = unquote(ref[1:])
            if fragment and fragment not in parser.ids:
                errors.append(f"index.html:{line}: missing fragment target #{fragment}")
            continue

        local_path = unquote(parsed.path)
        if local_path.startswith("/"):
            errors.append(
                f"index.html:{line}: root-absolute path '{ref}' may break on project GitHub Pages"
            )
            continue

        target = (ROOT / local_path).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"index.html:{line}: path escapes repository: {ref}")
            continue

        if not target.exists():
            errors.append(f"index.html:{line}: missing local file: {local_path}")

    required = [
        ROOT / "styles.css",
        ROOT / "script.js",
        ROOT / "assets" / "emcr2028-logo.png",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    if errors:
        print("Site validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Site validation passed.")
    print(f"Checked {len(parser.refs)} href/src references and {len(parser.ids)} HTML ids.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
