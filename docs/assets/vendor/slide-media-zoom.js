/* Powiększanie grafik i diagramów na slajdach.
 * Kliknięcie obrazu lub diagramu Mermaid otwiera go na całym ekranie; Esc zamyka.
 */
(() => {
  "use strict";
  let overlay;

  const close = () => {
    if (!overlay) return;
    overlay.remove();
    overlay = null;
    document.body.classList.remove("media-zoom-open");
  };

  const open = (source) => {
    close();
    overlay = document.createElement("div");
    overlay.className = "media-zoom-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-label", "Powiększona grafika — kliknij lub naciśnij Escape, aby zamknąć");
    const clone = source.cloneNode(true);
    clone.removeAttribute("width");
    clone.removeAttribute("height");
    clone.style.cssText = "";
    overlay.appendChild(clone);
    const hint = document.createElement("div");
    hint.className = "media-zoom-hint";
    hint.textContent = "Kliknij lub naciśnij Esc, aby zamknąć";
    overlay.appendChild(hint);
    overlay.addEventListener("click", close);
    document.body.appendChild(overlay);
    document.body.classList.add("media-zoom-open");
  };

  document.addEventListener("click", (event) => {
    if (overlay) return;
    const target = event.target.closest(
      ".reveal .slides section img, " +
      ".reveal .slides section svg[id^='mermaid-figure'], " +
      ".reveal .slides section svg.flowchart, " +
      ".reveal .slides section .mermaid svg"
    );
    if (!target || target.closest(".controls")) return;
    event.preventDefault();
    event.stopPropagation();
    open(target);
  }, true);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && overlay) {
      event.preventDefault();
      event.stopImmediatePropagation();
      close();
    }
  }, true);
})();
