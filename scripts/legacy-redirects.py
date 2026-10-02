#!/usr/bin/env python3
"""Quarto post-render: keep the old lecture URLs working.

GitHub Pages publishes docs/ as the site root; the previous site is copied to
docs/archiwum/. Old decks were linked (e.g. from Moodle) both as
<site>/wyklad_1.html and, while Pages served the repo root, as
<site>/docs/wyklad_1.html. Each old address gets a small page that forwards to
the archived copy, keeping the #/slide anchor.
"""
import html
import os
from pathlib import Path

# Old pages, relative to docs/ and to archiwum/ (same layout in both).
OLD_PAGES = [
    "wyklad_intro_1.html",
    "wyklad_intro_2.html",
    "wyklad_1.html",
    "wyklad_2.html",
    "wyklad_3.html",
    "konspekt.html",
    "lectures_en/lecture_01_fundamentals.html",
    "lectures_en/lecture_02_communication.html",
    "lectures_en/lecturer_notes.html",
    "lectures_en/presentation_descriptions.html",
]

TEMPLATE = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<title>Przeniesiono</title>
<link rel="canonical" href="{target}">
<script>location.replace({target_js} + location.hash);</script>
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
<p>Ta prezentacja została przeniesiona do archiwum: <a href="{target}">{target}</a>.</p>
</body>
</html>
"""


def write(dest: Path, target: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(TEMPLATE.format(target=html.escape(target), target_js=repr(target)), encoding="utf-8")


def main() -> None:
    out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
    for prefix in ("", "docs/"):
        for page in OLD_PAGES:
            rel = prefix + page
            write(out_dir / rel, "../" * rel.count("/") + "archiwum/" + page)
    # The former course landing page <site>/docs/ now lives at the site root.
    write(out_dir / "docs" / "index.html", "../")
    print(f"legacy-redirects: {2 * len(OLD_PAGES) + 1} pages")


if __name__ == "__main__":
    main()
