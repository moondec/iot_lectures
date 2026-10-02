/*
 * Show a fragment in the same step as another one.
 *
 * Usage in .qmd:
 *   * []{#k-ashton}Kevin Ashton …            <- target inside an incremental list item
 *   ::: {.fragment data-razem-z="k-ashton"}  <- appears together with that item
 *
 * Reveal.js numbers unindexed fragments in DOM order, so an element placed after a
 * list would appear last. Giving every fragment an explicit index in Markdown is
 * impractical for incremental lists, so after Reveal has numbered them we copy the
 * target's index and let Reveal re-sort the slide.
 */
(function () {
  function link() {
    var moved = new Set();
    document.querySelectorAll('[data-razem-z]').forEach(function (el) {
      var target = document.getElementById(el.getAttribute('data-razem-z'));
      var frag = target && target.closest('.fragment');
      if (!frag || !frag.hasAttribute('data-fragment-index')) return;
      el.setAttribute('data-fragment-index', frag.getAttribute('data-fragment-index'));
      moved.add(el.closest('section'));
    });
    moved.forEach(function (slide) {
      if (slide && window.Reveal && Reveal.syncFragments) Reveal.syncFragments(slide);
    });
  }
  function init() {
    if (!window.Reveal) return;
    if (Reveal.isReady && Reveal.isReady()) link();
    else Reveal.on('ready', link);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
