#!/usr/bin/env python3
"""One page holding every changed block of the docs, editable, saved in place.

    python3 tools/review.py            # against HEAD, on http://127.0.0.1:8002
    python3 tools/review.py origin/main

Each block is the markdown itself. Ctrl+S in a box writes it back to its file,
which the running `mkdocs serve` picks up, so the rendered page follows. The
diff is re-read on every load, so a block edited until it matches the base
simply leaves the page.
"""

import hashlib
import html
import json
import re
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hooks"))
import review as hook          # the mkdocs hook, for the diff and the blocks

BASE = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8002
DOCS = "http://127.0.0.1:8001/"


def doc_url(src: str) -> str:
    """docs/a/b.md -> the address mkdocs serves it at."""
    rel = src[len("docs/"):]
    if rel.endswith("index.md"):
        return DOCS + rel[:-len("index.md")]
    return DOCS + rel[:-3] + "/"


def slug(title: str) -> str:
    """the id python-markdown's toc gives a heading: punctuation dropped, not
    turned into a separator, so "the shader's world space" keeps "shaders"."""
    t = re.sub(r"[`*_\[\]()]", "", title).strip().lower()
    t = re.sub(r"[^\w\s-]", "", t)
    return re.sub(r"[-\s]+", "-", t).strip("-")


def collect():
    """[(src, [(text, anchor), ...])], the changed blocks of every touched page."""
    hook.BASE = BASE
    hook._scan()
    out = []
    for src in sorted(hook._changed):
        f = ROOT / src
        if not f.exists():
            continue
        text = f.read_text()
        touched = hook._changed[src]
        blocks, anchor = [], ""
        for first, last, block in hook._blocks(text):
            if block[0].startswith("#"):
                anchor = slug(block[0].lstrip("#"))
            if touched.intersection(range(first, last + 1)):
                blocks.append(("\n".join(block), anchor))
        if blocks:
            out.append((src, blocks))
    # the pages carrying the most first, so a rename of one word never buries a
    # page that was written from scratch
    out.sort(key=lambda p: (-sum(len(b) for b, _ in p[1]), p[0]))
    return out


DICT = ROOT / "tools" / "review.dict"

# what is not prose: fenced code, inline code, urls, link targets, html, and the
# yaml key of a deck example
_STRIP = [
    re.compile(r"^```.*?^```", re.S | re.M),
    re.compile(r"^~~~.*?^~~~", re.S | re.M),
    re.compile(r"`[^`]*`"),
    re.compile(r"https?://\S+"),
    re.compile(r"\]\([^)]*\)"),
    re.compile(r"<[^>]+>"),
]


def prose(text: str) -> str:
    for r in _STRIP:
        text = r.sub(" ", text)
    return text


def known() -> set:
    """the words this project uses that a dictionary does not have."""
    if not DICT.exists():
        return set()
    return {w.strip().lower() for w in DICT.read_text().splitlines() if w.strip()}


def misspelled(blocks: list) -> list:
    """one aspell pass for the whole page, then the words of each block."""
    import subprocess
    words = re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
    texts = [prose(t) for t, _ in blocks]
    try:
        out = subprocess.run(["aspell", "--lang=en", "--encoding=utf-8", "list"],
                             input="\n".join(texts), capture_output=True, text=True)
        bad = {w for w in out.stdout.split() if w}
    except FileNotFoundError:
        return [[] for _ in blocks]
    ok = known()

    def project(w):
        w = w.lower()
        return w in ok or (w.endswith("'s") and w[:-2] in ok)

    bad = {w for w in bad if not project(w)}
    return [sorted({w for w in words.findall(t) if w in bad}) for t in texts]


CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #14161a; color: #d8dae0; font: 13px/1.5 ui-monospace,
       SFMono-Regular, Menlo, monospace; }
header { position: sticky; top: 0; background: #1b1e24; border-bottom: 1px solid #2c313a;
         padding: .6rem 1rem; display: flex; gap: 1rem; align-items: baseline; z-index: 2;
         flex-wrap: wrap; }
header b { color: #e0a300; } header span { color: #7d8593; }
main { max-width: 60rem; margin: 0 auto; padding: 1rem 1rem 6rem; }
h2 { font-size: 13px; margin: 2rem 0 .5rem; color: #9fb4d0; font-weight: 600; }
h2 a { color: #5a6675; text-decoration: none; float: right; font-weight: 400; }
h2 a:hover { color: #e0a300; }
h2 .n { color: #5a6675; font-weight: 400; }
section.hidden, section.gone { display: none; }
#filter { background: #14161a; color: #d8dae0; border: 1px solid #3a414c; border-radius: 3px;
          padding: .15rem .5rem; font: inherit; width: 12rem; }
.block { position: relative; margin: .5rem 0; }
.block.gone { display: none; }
body.show-hidden .block.gone { display: block; opacity: .45; }
textarea { width: 100%; background: #1b1e24; color: #d8dae0; border: 1px solid #2c313a;
           border-left: 3px solid #e0a300; border-radius: 3px; padding: .6rem .7rem;
           font: inherit; resize: vertical; tab-size: 4; }
textarea:focus { outline: none; border-color: #3d7fbf; border-left-color: #e0a300; }
.block.dirty textarea { border-color: #b46a00; }
.block.saved textarea { border-left-color: #3fa34d; }
.tag { position: absolute; right: 3.4rem; top: -.1rem; font-size: 11px; color: #7d8593; }
.jump, .hide { position: absolute; top: -.15rem; font-size: 12px; color: #5a6675;
               text-decoration: none; cursor: pointer; background: none; border: 0;
               padding: 0 .25rem; font-family: inherit; }
.jump { right: 1.6rem; } .hide { right: .3rem; }
.jump:hover, .hide:hover { color: #e0a300; }
.spell { font-size: 11px; color: #7d8593; margin: .15rem 0 0 .2rem; }
.spell b { color: #d08770; font-weight: 400; cursor: pointer; border-bottom: 1px dotted #6b5340; }
.spell b:hover { color: #e0a300; }
.err { color: #e06a6a; }
footer { position: fixed; bottom: 0; left: 0; right: 0; background: #1b1e24;
         border-top: 1px solid #2c313a; padding: .5rem 1rem; font-size: 12px;
         display: flex; gap: .6rem; align-items: center; }
footer span { color: #7d8593; }
button { background: #2c313a; color: #d8dae0; border: 1px solid #3a414c; border-radius: 3px;
         padding: .25rem .7rem; font: inherit; cursor: pointer; }
button:hover { border-color: #e0a300; }
"""

JS = """
const HIDDEN = 'docReviewHidden';
function hiddenSet() { try { return new Set(JSON.parse(localStorage.getItem(HIDDEN) || '[]')); }
                       catch (e) { return new Set(); } }
function storeHidden(s) { localStorage.setItem(HIDDEN, JSON.stringify([...s])); }
function mark(el, cls, msg) {
  const b = el.closest('.block');
  b.className = 'block ' + cls + (b.dataset.gone === '1' ? ' gone' : '');
  b.querySelector('.tag').textContent = msg || '';
}
function note(msg) { document.getElementById('note').textContent = msg; }
async function save(ta) {
  const r = await fetch('/save', {method: 'POST', body: JSON.stringify(
      {file: ta.dataset.file, original: ta.dataset.original, text: ta.value})});
  const j = await r.json();
  if (j.ok) { ta.dataset.original = ta.value; mark(ta, 'saved', 'saved'); }
  else mark(ta, 'dirty', j.error);
  return j.ok;
}
async function saveAll() {
  const boxes = [...document.querySelectorAll('.dirty textarea')];
  if (!boxes.length) { note('nothing edited'); return; }
  let n = 0;
  for (const ta of boxes) if (await save(ta)) n++;
  note(n + ' of ' + boxes.length + ' blocks written');
}
async function addWord(el) {
  const w = el.dataset.w;
  await fetch('/dict', {method: 'POST', body: JSON.stringify({word: w})});
  for (const b of document.querySelectorAll('.spell b'))
    if (b.dataset.w === w) b.remove();
  note('"' + w + '" added to tools/review.dict');
}
function hide(btn) {
  const b = btn.closest('.block'), s = hiddenSet();
  if (b.dataset.gone === '1') { s.delete(b.dataset.id); b.dataset.gone = '0'; b.classList.remove('gone'); }
  else { s.add(b.dataset.id); b.dataset.gone = '1'; b.classList.add('gone'); }
  storeHidden(s); count();
}
function hideFile(link) {
  const s = hiddenSet();
  for (const b of link.closest('section').querySelectorAll('.block')) {
    s.add(b.dataset.id); b.dataset.gone = '1'; b.classList.add('gone');
  }
  storeHidden(s); count();
}
function count() {
  const n = document.querySelectorAll('.block.gone').length;
  document.getElementById('hidden-count').textContent = n;
  for (const s of document.querySelectorAll('section'))
    s.classList.toggle('gone', !document.body.classList.contains('show-hidden') &&
        [...s.querySelectorAll('.block')].every(b => b.dataset.gone === '1'));
}
function showHidden(on) { document.body.classList.toggle('show-hidden', on); count(); }
function fit(ta) { ta.style.height = 'auto'; ta.style.height = (ta.scrollHeight + 4) + 'px'; }
function filter(q) {
  q = q.toLowerCase();
  for (const s of document.querySelectorAll('section'))
    s.classList.toggle('hidden', q && !s.dataset.file.toLowerCase().includes(q));
}
document.addEventListener('DOMContentLoaded', () => {
  const s = hiddenSet();
  for (const b of document.querySelectorAll('.block'))
    if (s.has(b.dataset.id)) { b.dataset.gone = '1'; b.classList.add('gone'); }
  for (const ta of document.querySelectorAll('textarea')) {
    fit(ta);
    ta.addEventListener('input', () => { fit(ta);
      mark(ta, ta.value === ta.dataset.original ? '' : 'dirty',
           ta.value === ta.dataset.original ? '' : 'edited'); });
  }
  count();
});
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 's') { e.preventDefault(); saveAll(); }
});
"""


def page() -> bytes:
    files = collect()
    flat = [b for _, blocks in files for b in blocks]
    spell = misspelled(flat)
    n, i = len(flat), 0
    body = []
    for src, blocks in files:
        body.append('<section data-file="{}"><h2>{} <span class="n">{}</span>'
                    ' <a href="{}" target="slopedoc">open \u2197</a>'
                    ' <a onclick="hideFile(this)">hide all</a></h2>'
                    .format(html.escape(src), html.escape(src),
                            "{} blocks".format(len(blocks)) if len(blocks) > 1 else "",
                            doc_url(src)))
        for text, anchor in blocks:
            esc = html.escape(text)
            # the word rides in an attribute, so an apostrophe cannot break the call
            bad = "".join('<b data-w="{0}" onclick="addWord(this)" title="add to '
                          'tools/review.dict">{0}</b> '.format(html.escape(w))
                          for w in spell[i])
            body.append(
                '<div class="block" data-id="{}" data-gone="0">'
                '<span class="tag"></span>'
                '<a class="jump" href="{}{}" target="slopedoc">\u2197</a>'
                '<button class="hide" onclick="hide(this)" title="hide this block">'
                '\u00d7</button>'
                '<textarea spellcheck="false" data-file="{}" data-original="{}">{}</textarea>'
                '{}</div>'.format(
                    # stable across restarts, so a hidden block stays hidden
                    "{}:{}".format(html.escape(src),
                                   hashlib.md5(text.encode()).hexdigest()[:12]),
                    doc_url(src), "#" + anchor if anchor else "",
                    html.escape(src), esc, esc,
                    '<div class="spell">' + bad + '</div>' if bad else ""))
            i += 1
        body.append('</section>')
    if not files:
        body.append("<p>nothing changed against <b>{}</b>.</p>".format(html.escape(BASE)))
    suspect = sum(len(w) for w in spell)
    return ("<!doctype html><meta charset='utf-8'><title>doc review</title>"
            "<style>{}</style><script>{}</script>"
            "<header><b>{} blocks</b><span>changed against {}</span>"
            "<input id='filter' placeholder='filter by path' oninput='filter(this.value)'>"
            "<span>{} words to check</span>"
            "<label><input type='checkbox' onchange='showHidden(this.checked)'> show the "
            "<span id='hidden-count'>0</span> hidden</label>"
            "<span>ctrl+s writes every edited block</span></header>"
            "<main>{}</main>"
            "<footer><button onclick='saveAll()'>save all (ctrl+s)</button> "
            "<button onclick='location.reload()'>re-read the diff</button>"
            "<span id='note'></span></footer>"
            .format(CSS, JS, n, html.escape(BASE), suspect, "".join(body))).encode()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, page())

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/dict":
            word = re.sub(r"[^A-Za-z'-]", "", req.get("word", ""))
            if word:
                with DICT.open("a") as f:
                    f.write(word + "\n")
            self._send(200, json.dumps({"ok": bool(word)}).encode(), "application/json")
            return
        f = ROOT / req["file"]
        answer = {"ok": False, "error": "unknown file"}
        if f.is_file() and str(f).startswith(str(ROOT / "docs")):
            text = f.read_text()
            hits = text.count(req["original"])
            if hits == 1:
                f.write_text(text.replace(req["original"], req["text"], 1))
                answer = {"ok": True}
            elif hits == 0:
                answer["error"] = "the file changed under this block, re-read the diff"
            else:
                answer["error"] = "this text appears {} times, edit the file".format(hits)
        self._send(200, json.dumps(answer).encode(), "application/json")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("review of {} on http://127.0.0.1:{}/".format(BASE, PORT))
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
