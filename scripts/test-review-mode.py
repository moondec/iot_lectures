#!/usr/bin/env python3
"""Testuje tła, pełnoekranowe powiększanie oraz tryb recenzji ?review=1."""
import functools
import http.server
import json
import os
import socketserver
import threading

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PORT = int(os.environ.get("REVIEW_TEST_PORT", "8097"))
DECKS = {
    "00-internet-przyszlosci": ("tlo-blue", "background-blue.jpg"),
    "01-architektura-i-wymagania": ("tlo-orange", "background-orange.jpg"),
    "02-urzadzenie-sensory-energia": ("tlo-orange", "background-orange.jpg"),
    "03-lacznosc-i-ota": ("tlo-green", "background-green.jpg"),
    "04-mqtt-i-kontrakt-danych": ("tlo-green", "background-green.jpg"),
    "05-brzeg-node-red-sheets": ("tlo-green", "background-green.jpg"),
    "06-thingsboard-ce": ("tlo-blue", "background-blue.jpg"),
    "07-odpornosc-bezpieczenstwo-eksploatacja": ("tlo-blue", "background-blue.jpg"),
}


def server():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="docs")
    handler.log_message = lambda *args, **kwargs: None
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    srv = server()
    results = {"backgrounds": [], "contrast": [], "zoom": None,
               "review": None, "errors": []}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=os.environ.get("AGENT_BROWSER_EXECUTABLE_PATH"))
            page = browser.new_page(viewport={"width": 1440, "height": 810})
            failed = []
            page.on("response", lambda r: failed.append(f"HTTP {r.status} {r.url}")
                    if r.status >= 400 else None)

            for deck, (body_class, image) in DECKS.items():
                page.goto(f"http://127.0.0.1:{PORT}/slides/{deck}.html",
                          wait_until="networkidle")
                page.wait_for_function("window.Reveal && Reveal.isReady()")
                body_ok = page.locator("body").evaluate(
                    "(el, cls) => el.classList.contains(cls)", body_class)
                bg = page.evaluate("""() => {
                    const all = document.querySelectorAll('.backgrounds .slide-background-content');
                    return all.length > 1 ? getComputedStyle(all[1]).backgroundImage : '';
                }""")
                ok = body_ok and image in bg
                results["backgrounds"].append(
                    {"deck": deck, "class": body_class, "image": image, "ok": ok})
                if not ok:
                    results["errors"].append(f"Brak tła: {deck}: {bg}")

                contrast = page.evaluate("""() => {
                    const rgb = value => {
                        const match = value.match(/[\\d.]+/g);
                        return match ? match.slice(0, 4).map(Number) : [0, 0, 0, 0];
                    };
                    const luminance = color => {
                        const linear = value => {
                            value /= 255;
                            return value <= 0.04045 ? value / 12.92
                                : Math.pow((value + 0.055) / 1.055, 2.4);
                        };
                        return 0.2126 * linear(color[0]) + 0.7152 * linear(color[1])
                            + 0.0722 * linear(color[2]);
                    };
                    const brightText = [];
                    const sectionProblems = [];
                    for (const slide of Reveal.getSlides()) {
                        const isSection = slide.classList.contains('sekcja');
                        const background = Reveal.getSlideBackground(slide);
                        const content = background?.querySelector('.slide-background-content');
                        if (isSection) {
                            const heading = slide.querySelector('h1, h2');
                            const outer = rgb(getComputedStyle(background).backgroundColor);
                            const text = heading ? rgb(getComputedStyle(heading).color) : [0, 0, 0, 0];
                            const image = content ? getComputedStyle(content).backgroundImage : '';
                            if (luminance(outer) >= 0.35 || luminance(text) <= 0.72 || image !== 'none') {
                                sectionProblems.push({slide: slide.id, image});
                            }
                        }
                        for (const element of slide.querySelectorAll('*')) {
                            const hasDirectText = [...element.childNodes].some(node =>
                                node.nodeType === 3 && node.textContent.trim());
                            if (!hasDirectText) continue;
                            const color = rgb(getComputedStyle(element).color);
                            if ((color[3] ?? 1) < 0.5 || luminance(color) < 0.72) continue;
                            let onDark = isSection;
                            for (let ancestor = element; ancestor && ancestor !== slide && !onDark;
                                 ancestor = ancestor.parentElement) {
                                const backgroundColor = rgb(getComputedStyle(ancestor).backgroundColor);
                                if ((backgroundColor[3] ?? 0) > 0.5
                                    && luminance(backgroundColor) < 0.35) onDark = true;
                            }
                            if (!onDark) brightText.push({
                                slide: slide.id, tag: element.tagName,
                                text: element.textContent.trim().slice(0, 100)
                            });
                        }
                    }
                    return {brightText, sectionProblems};
                }""")
                contrast_ok = not contrast["brightText"] and not contrast["sectionProblems"]
                results["contrast"].append({"deck": deck, **contrast, "ok": contrast_ok})
                if not contrast_ok:
                    results["errors"].append(f"Problem kontrastu: {deck}: {contrast}")

            # Powiększanie grafiki i zamknięcie Escape.
            page.goto(f"http://127.0.0.1:{PORT}/slides/01-architektura-i-wymagania.html#/skala",
                      wait_until="networkidle")
            page.wait_for_function("window.Reveal && Reveal.isReady()")
            page.locator("#skala img").click()
            opened = page.locator(".media-zoom-overlay").is_visible()
            page.keyboard.press("Escape")
            closed = page.locator(".media-zoom-overlay").count() == 0
            results["zoom"] = {"opened": opened, "closed_with_escape": closed,
                               "ok": opened and closed}
            if not results["zoom"]["ok"]:
                results["errors"].append("Powiększenie grafiki nie działa")

            # Tryb recenzji: zaznaczenie, komentarz, localStorage i trwałość po reloadzie.
            page.goto(f"http://127.0.0.1:{PORT}/slides/01-architektura-i-wymagania.html?review=1#/cele",
                      wait_until="networkidle")
            page.wait_for_function("window.Reveal && Reveal.isReady()")
            page.wait_for_selector("#review-toolbar")
            page.evaluate("""() => {
                const el = document.querySelector('#cele .lead');
                const r = document.createRange(); r.selectNodeContents(el);
                const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
            }""")
            page.once("dialog", lambda d: d.accept("Zwiększyć kontrast tego zdania."))
            page.locator("#review-toolbar [data-action=add]").click()
            stored = page.evaluate(
                "JSON.parse(localStorage.getItem('iot-course-slides-review-v1') || '[]')")
            page.reload(wait_until="networkidle")
            page.wait_for_selector("#review-toolbar")
            persisted = "1 uwag" in page.locator("#review-toolbar .review-count").inner_text()
            record_ok = (len(stored) == 1 and stored[0]["slide"] == "cele"
                         and bool(stored[0]["quote"])
                         and stored[0]["comment"] == "Zwiększyć kontrast tego zdania.")
            page.once("dialog", lambda d: d.accept())
            page.locator("#review-toolbar [data-action=clear]").click()
            cleared = page.evaluate(
                "JSON.parse(localStorage.getItem('iot-course-slides-review-v1') || '[]')") == []
            results["review"] = {"record_ok": record_ok, "persisted": persisted,
                                 "cleared": cleared,
                                 "ok": record_ok and persisted and cleared}
            if not results["review"]["ok"]:
                results["errors"].append("Tryb recenzji nie zapisał, nie odtworzył lub nie wyczyścił uwagi")
            page.evaluate("localStorage.removeItem('iot-course-slides-review-v1')")

            if failed:
                results["errors"].extend(failed)
            browser.close()
    finally:
        srv.shutdown()

    results["ok"] = not results["errors"]
    with open("review/verification-review-mode.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    raise SystemExit(0 if results["ok"] else 1)


if __name__ == "__main__":
    main()
