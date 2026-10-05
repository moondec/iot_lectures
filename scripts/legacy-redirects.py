#!/usr/bin/env python3
"""Quarto post-render: keep the old lecture URLs working.

GitHub Pages publishes docs/ as the site root; the previous site is copied to
docs/archiwum/. Old decks were linked (e.g. from Moodle) both as
<site>/wyklad_1.html and, while Pages served the repo root, as
<site>/docs/wyklad_1.html. Each old address gets a small page that forwards to
the archived copy, keeping the #/slide anchor.

Decks renumbered or removed in the 2026-10-05 restructure (Node-RED / Google
Sheets module dropped) forward to their current URLs in slides/. A moved deck
keeps the #/slide anchor (slide ids are unchanged); the removed deck forwards
to the start of the closest remaining lecture (04, data contract), because its slide ids
do not exist there.
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

# Old deck path (relative to docs/) -> (new path relative to docs/, keep #/slide anchor)
MOVED_DECKS = {
    "slides/05-brzeg-node-red-sheets.html": ("slides/04-mqtt-i-kontrakt-danych.html", False),
    "slides/06-thingsboard-ce.html": ("slides/05-thingsboard-ce.html", True),
    "slides/07-odpornosc-bezpieczenstwo-eksploatacja.html": ("slides/06-odpornosc-bezpieczenstwo-eksploatacja.html", True),
}

TEMPLATE = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<title>Przeniesiono</title>
<link rel="canonical" href="{target}">
<script>location.replace({target_js}{hash_js});</script>
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
<p>{message}: <a href="{target}">{target}</a>.</p>
</body>
</html>
"""


def write(dest: Path, target: str, keep_hash: bool = True,
          message: str = "Ta prezentacja została przeniesiona do archiwum") -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(TEMPLATE.format(target=html.escape(target), target_js=repr(target),
                                    hash_js=" + location.hash" if keep_hash else "",
                                    message=message), encoding="utf-8")


def main() -> None:
    out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
    for prefix in ("", "docs/"):
        for page in OLD_PAGES:
            rel = prefix + page
            write(out_dir / rel, "../" * rel.count("/") + "archiwum/" + page)
    # The former course landing page <site>/docs/ now lives at the site root.
    write(out_dir / "docs" / "index.html", "../")
    n = 2 * len(OLD_PAGES) + 1
    for prefix in ("", "docs/"):
        for old, (new, keep_hash) in MOVED_DECKS.items():
            rel = prefix + old
            target = "../" * rel.count("/") + new
            msg = ("Ten wykład ma nowy numer i adres" if keep_hash
                   else "Ten wykład usunięto z kursu. Najbliższy temat omawia wykład")
            write(out_dir / rel, target, keep_hash, msg)
            n += 1
    print(f"legacy-redirects: {n} pages")


if __name__ == "__main__":
    main()
