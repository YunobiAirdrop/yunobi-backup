// Descript script-edit page helpers.
// Install once per tab:  orca eval --page "$PAGE" --expression "$(cat helpers.js)" --json
// Assumes the viewport has been grown so the whole script fits (see SKILL.md law 7).
(function () {
  var W = window;

  W.__ed = [].slice
    .call(document.querySelectorAll('.public-DraftEditor-content'))
    .find(function (e) { return (e.innerText || '').length > 500; });

  W.__blocks = function () {
    return [].slice.call(W.__ed.querySelectorAll('[data-block="true"]'));
  };

  // Flat char-offset map over a block's text nodes. Lets us address a range by
  // substring without caring how Descript splits words into spans.
  W.__map = function (block) {
    var w = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
    var s = '', parts = [], n;
    while ((n = w.nextNode())) {
      parts.push({ node: n, start: s.length, end: s.length + n.data.length });
      s += n.data;
    }
    return { text: s, parts: parts };
  };

  // Law 4: ignored words stay in the DOM, struck through. Skip them.
  W.__ignored = function (node) {
    var e = node.nodeType === 3 ? node.parentElement : node;
    while (e && e !== W.__ed) {
      if (getComputedStyle(e).textDecorationLine.indexOf('line-through') !== -1) return true;
      e = e.parentElement;
    }
    return false;
  };

  // Returns viewport CSS-pixel coordinates for a drag across `needle`.
  // Uses one-character ranges: a collapsed range gives an unreliable rect.
  // Pass `bIdx` to confine the search to one block. Required for any needle
  // short or repeated enough to occur in more than one paragraph.
  W.__find = function (needle, bIdx) {
    var bs = W.__blocks();
    var lo = 0, hi = bs.length;
    if (typeof bIdx === 'number') { lo = bIdx; hi = Math.min(bIdx + 1, bs.length); }
    for (var bi = lo; bi < hi; bi++) {
      var m = W.__map(bs[bi]), from = 0, i;
      while ((i = m.text.indexOf(needle, from)) >= 0) {
        var j = i + needle.length;
        var a = m.parts.find(function (p) { return i >= p.start && i < p.end; });
        var z = m.parts.find(function (p) { return j - 1 >= p.start && j - 1 < p.end; });
        if (a && z && !W.__ignored(a.node)) {
          var r1 = document.createRange();
          r1.setStart(a.node, i - a.start);
          r1.setEnd(a.node, Math.min(i - a.start + 1, a.node.data.length));
          var r2 = document.createRange();
          r2.setStart(z.node, j - 1 - z.start);
          r2.setEnd(z.node, Math.min(j - z.start, z.node.data.length));
          var q1 = r1.getClientRects()[0], q2 = r2.getClientRects()[0];
          if (!q1 || !q2) { from = i + 1; continue; }
          return {
            ok: true,
            sx: Math.round(q1.left), sy: Math.round(q1.top + q1.height / 2),
            ex: Math.round(q2.right), ey: Math.round(q2.top + q2.height / 2),
            top: Math.round(q1.top), bottom: Math.round(q2.bottom),
            onscreen: q1.top > 60 && q2.bottom < innerHeight - 60
          };
        }
        from = i + 1;
      }
    }
    return { ok: false };
  };

  // Law 6: only ignore when the live selection IS the intended text.
  W.__igIfSync = function (expected) {
    var norm = function (s) { return s.replace(/\s+/g, ' ').trim(); };
    var sel = W.getSelection().toString();
    if (norm(sel) !== norm(expected)) {
      return { clicked: false, mismatch: true, gotLen: sel.length, got: sel.slice(0, 50) };
    }
    var b = document.querySelector('[data-testid="selection-toolbar-ignore-button"]');
    if (!b) return { clicked: false, toolbarMissing: true, len: sel.length };
    b.click();
    return { clicked: true, len: sel.length };
  };

  return 'helpers installed, blocks=' + W.__blocks().length;
})()
