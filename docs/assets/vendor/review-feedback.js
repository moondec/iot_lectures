/* Tryb recenzji prezentacji: ?review=1
 * Zapisuje uwagi lokalnie w przeglądarce i eksportuje je jako Markdown/JSON.
 */
(() => {
  "use strict";
  const params = new URLSearchParams(window.location.search);
  if (params.get("review") !== "1") return;

  const STORAGE_KEY = "iot-course-slides-review-v1";
  const deck = decodeURIComponent(location.pathname.split("/").pop().replace(/\.html$/, ""));
  let notes = [];
  try { notes = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"); } catch (_) { notes = []; }

  const save = () => localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
  const current = () => {
    const slide = window.Reveal?.getCurrentSlide();
    const idx = window.Reveal?.getIndices() || {};
    return { slide, id: slide?.id || `slajd-${idx.h ?? 0}-${idx.v ?? 0}`, fragment: idx.f ?? null };
  };
  const selectedText = () => (window.getSelection()?.toString() || "").trim().replace(/\s+/g, " ");

  const toolbar = document.createElement("div");
  toolbar.id = "review-toolbar";
  toolbar.innerHTML = `
    <span class="review-label">Tryb recenzji</span>
    <button type="button" data-action="add" title="Zaznacz tekst i dodaj uwagę (C)">💬 Dodaj uwagę</button>
    <button type="button" data-action="copy" title="Kopiuj wszystkie uwagi jako Markdown">Kopiuj</button>
    <button type="button" data-action="download" title="Pobierz uwagi jako pliki Markdown i JSON">Pobierz</button>
    <button type="button" data-action="clear" title="Usuń wszystkie lokalne uwagi">Wyczyść</button>
    <span class="review-count" aria-live="polite"></span>`;
  document.body.appendChild(toolbar);

  const markdown = () => {
    const rows = notes.map((n, i) => {
      const frag = n.fragment === null ? "" : `, fragment ${n.fragment}`;
      const quote = n.quote ? `\n> ${n.quote.replace(/\n/g, " ")}\n` : "";
      return `## ${i + 1}. ${n.deck} — #${n.slide}${frag}\n${quote}\n${n.comment}\n`;
    });
    return `# Uwagi do prezentacji IoT\n\nEksport: ${new Date().toISOString()}\n\n${rows.join("\n")}`;
  };

  const refresh = () => {
    const { id } = current();
    const all = notes.length;
    const here = notes.filter(n => n.deck === deck && n.slide === id).length;
    toolbar.querySelector(".review-count").textContent = `${all} uwag · ten slajd: ${here}`;
    document.body.classList.add("review-mode");
  };

  const add = () => {
    const { id, fragment } = current();
    const quote = selectedText();
    const promptText = quote
      ? `Uwaga do #${id}\nZaznaczenie: „${quote.slice(0, 180)}${quote.length > 180 ? "…" : ""}”`
      : `Uwaga do całego slajdu #${id}`;
    const comment = window.prompt(promptText, "");
    if (!comment?.trim()) return;
    notes.push({
      deck, slide: id, fragment, quote,
      comment: comment.trim(),
      url: `${location.origin}${location.pathname}?review=1#/${id}`,
      created_at: new Date().toISOString()
    });
    save();
    refresh();
  };

  const download = (name, text, type) => {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type }));
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };

  toolbar.addEventListener("click", async (event) => {
    const action = event.target.closest("button")?.dataset.action;
    if (action === "add") add();
    if (action === "copy") {
      await navigator.clipboard.writeText(markdown());
      const old = event.target.textContent;
      event.target.textContent = "Skopiowano";
      setTimeout(() => { event.target.textContent = old; }, 1200);
    }
    if (action === "download") {
      const stamp = new Date().toISOString().slice(0, 10);
      download(`uwagi-iot-${stamp}.md`, markdown(), "text/markdown;charset=utf-8");
      download(`uwagi-iot-${stamp}.json`, JSON.stringify(notes, null, 2), "application/json;charset=utf-8");
    }
    if (action === "clear" && notes.length && window.confirm("Usunąć wszystkie lokalne uwagi?")) {
      notes = [];
      save();
      refresh();
    }
  });

  document.addEventListener("keydown", (event) => {
    if ((event.key === "c" || event.key === "C") && !/INPUT|TEXTAREA/.test(event.target.tagName)) {
      event.preventDefault();
      add();
    }
  });

  const ready = () => {
    refresh();
    window.Reveal?.on("slidechanged", refresh);
    window.Reveal?.on("fragmentshown", refresh);
    window.Reveal?.on("fragmenthidden", refresh);
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready);
  else ready();
})();
