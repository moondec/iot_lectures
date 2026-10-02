#!/usr/bin/env python3
"""Quarto post-render: keep the old lecture URLs working.

The previous site served its decks from docs/ (e.g. docs/wyklad_1.html#/slide).
Moodle pages link there, so after the move to archiwum/ each old address gets a
small page that forwards to the archived copy, keeping the #/slide anchor.
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


def main() -> None:
    out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
    for page in OLD_PAGES:
        depth = page.count("/") + 1  # docs/ itself plus any subfolders
        target = "../" * depth + "archiwum/" + page
        dest = out_dir / page
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            TEMPLATE.format(target=html.escape(target), target_js=repr(target)),
            encoding="utf-8",
        )
    print(f"legacy-redirects: {len(OLD_PAGES)} pages")


if __name__ == "__main__":
    main()
