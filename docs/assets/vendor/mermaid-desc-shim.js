/*
 * mermaid-desc-shim.js — obejście błędu w skrypcie Quarto
 * site_libs/quarto-diagram/mermaid-postprocess-shim.js.
 *
 * Objaw: w konsoli przeglądarki pojawia się
 *   TypeError: Cannot read properties of null (reading 'id')
 *
 * Przyczyna: skrypt Quarto wykonuje na zdarzeniu `load`
 *   document.querySelectorAll("div.cell-output-display svg")
 *     .filter(el => el.querySelector("desc").id.startsWith("chart-desc-mermaid"))
 * bez sprawdzenia, czy element <desc> w ogóle istnieje. Przy ustawieniu
 * `mermaid-format: svg` diagramy są renderowane po stronie budowania i
 * powstające SVG nie zawierają elementu <desc> — wyrażenie rzuca wyjątek,
 * który przerywa całą pętlę.
 *
 * Obejście: na zdarzeniu `DOMContentLoaded` (zawsze wcześniejszym od `load`)
 * dodajemy każdemu takiemu SVG pusty element <desc>. Filtr Quarto odczyta
 * wtedy pusty identyfikator, pominie element i nie zgłosi błędu.
 *
 * Pominięcie etapu postProcess jest tu poprawne: diagramy wyrenderowane
 * na etapie budowania mają już prawidłowy układ i nie wymagają korekty
 * pozycji etykiet wykonywanej przez skrypt Quarto dla renderu w przeglądarce.
 *
 * Do usunięcia, gdy błąd zostanie poprawiony w Quarto (sprawdzone w 1.10.18).
 */
(function () {
  "use strict";
  function uzupelnijDesc() {
    var svgs = document.querySelectorAll("div.cell-output-display svg");
    for (var i = 0; i < svgs.length; i++) {
      if (!svgs[i].querySelector("desc")) {
        var d = document.createElementNS("http://www.w3.org/2000/svg", "desc");
        d.setAttribute("id", "");
        svgs[i].insertBefore(d, svgs[i].firstChild);
      }
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", uzupelnijDesc);
  } else {
    uzupelnijDesc();
  }
})();
