"""Marks, in the served site, what changed against a git ref.

    DOC_BASE=HEAD mkdocs serve      # the default: everything not yet committed

Every markdown block holding a changed line is drawn with a coloured margin, and
a panel lists the pages that carry one. mkdocs rebuilds on save, so the marks
follow the working tree as it is edited: revert a paragraph and its mark goes.
"""

import os
import re
import subprocess
from pathlib import Path

BASE = os.environ.get("DOC_BASE", "HEAD")
ROOT = Path(__file__).resolve().parent.parent

# src_path -> set of changed line numbers, 1-based, in the working-tree file
_changed: dict[str, set[int]] = {}
# src_path -> (url, number of changed blocks), filled as pages are rendered
_pages: dict[str, list] = {}


def _git(*args: str) -> str:
    out = subprocess.run(("git", *args), cwd=ROOT, capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else ""


def _scan() -> None:
    """Changed lines of every doc, from the diff and from what git does not track."""
    _changed.clear()
    hunk = re.compile(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@")
    current = None
    for line in _git("diff", "-U0", "--no-color", BASE, "--", "docs").splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
        elif line.startswith("@@") and current:
            m = hunk.match(line)
            if m:
                start, count = int(m.group(1)), int(m.group(2) or 1)
                _changed.setdefault(current, set()).update(range(start, start + count))
    # -uall, or an untracked directory is listed as one line and its pages missed
    for line in _git("status", "--porcelain", "-uall", "--", "docs").splitlines():
        if line.startswith("?? "):
            f = ROOT / line[3:].strip()
            if f.suffix == ".md":
                n = len(f.read_text().splitlines())
                _changed["docs/" + str(f.relative_to(ROOT / "docs"))] = set(range(1, n + 2))


def _blocks(md: str):
    """(first, last) per markdown block, 1-based and inclusive.

    Blocks are separated by blank lines, fences are kept whole, and an indented
    block joins the one above it, so a tab keeps its content and a table its
    rows. Every block then starts at column 0 and can be wrapped in a div.
    """
    lines = md.split("\n")
    # a fence opens a block only when nothing else on the line uses its char,
    # so a line starting with `inline code` is not one
    fence_re = re.compile(r"^(\s*)(`{3,}|~{3,})([^`~]*)$")
    fence = None
    start = None
    raw = []
    for i, line in enumerate(lines, 1):
        m = fence_re.match(line)
        if m:
            if fence is None:
                fence = m.group(2)[0]
            elif m.group(2)[0] == fence and not m.group(3).strip():
                fence = None
        if not line.strip() and fence is None:
            if start:
                raw.append([start, i - 1])
            start = None
        elif start is None:
            start = i
    if start:
        raw.append([start, len(lines)])

    out = []
    for first, last in raw:
        if out and lines[first - 1][:1].isspace():
            out[-1][1] = last
        else:
            out.append([first, last])
    for first, last in out:
        yield first, last, lines[first - 1:last]


def on_config(config):
    _scan()
    for ext in ("md_in_html", "attr_list"):
        if ext not in config["markdown_extensions"]:
            config["markdown_extensions"].append(ext)
    return config


def on_page_markdown(markdown, page, config, files):
    src = "docs/" + page.file.src_uri
    touched = _changed.get(src)
    if not touched:
        return markdown
    # mkdocs strips the yaml front matter before this hook, so line numbers shift
    raw = Path(page.file.abs_src_path).read_text().split("\n")
    offset = len(raw) - len(markdown.split("\n"))

    md_lines = markdown.split("\n")
    out, marks, last_end = [], 0, 0
    for first, last, block in _blocks(markdown):
        # the blank lines between two blocks, kept as they were
        out.extend(md_lines[last_end:first - 1])
        last_end = last
        text = "\n".join(block)
        if touched.intersection(range(first + offset, last + offset + 1)):
            marks += 1
            out.append('<div class="doc-review" markdown="1">\n' + text + "\n</div>")
        else:
            out.append(text)
    out.extend(md_lines[last_end:])
    return "\n".join(out)


def on_files(files, config):
    """url, path and block count of every changed page, for the panel."""
    _pages.clear()
    for f in files.documentation_pages():
        touched = _changed.get("docs/" + f.src_uri)
        if not touched:
            continue
        text = Path(f.abs_src_path).read_text()
        n = sum(1 for first, last, _ in _blocks(text)
                if touched.intersection(range(first, last + 1)))
        _pages["docs/" + f.src_uri] = [f.url, f.src_uri, n]
    return files


_CSS = """
<style>
.doc-review { border-left: 3px solid #e0a300; padding-left: .8em; margin-left: -1.1em;
              background: rgba(224,163,0,.07); border-radius: 2px; }
body.doc-review-off .doc-review { border-left-color: transparent; background: none; }
#doc-review-panel { position: fixed; right: 1rem; bottom: 1rem; z-index: 20;
    max-width: 22rem; max-height: 60vh; overflow: auto; font-size: .72rem;
    background: var(--md-default-bg-color); color: var(--md-default-fg-color);
    border: 1px solid #e0a300; border-radius: 4px; padding: .5rem .7rem;
    box-shadow: 0 2px 12px rgba(0,0,0,.25); }
#doc-review-panel.folded ul, #doc-review-panel.folded .doc-review-hint { display: none; }
#doc-review-panel ul { list-style: none; margin: .4rem 0 0; padding: 0; }
#doc-review-panel li { margin: .15rem 0; }
#doc-review-panel b { cursor: pointer; }
#doc-review-panel .here { font-weight: 700; }
#doc-review-panel i { color: #e0a300; font-style: normal; }
</style>
"""


def on_post_page(output, page, config):
    if not _pages:
        return output
    rows = "".join(
        '<li><a href="/{}" class="{}">{} <i>{}</i></a></li>'.format(
            url, "here" if src == page.file.src_uri else "", src, n)
        for url, src, n in sorted(_pages.values(), key=lambda p: (-p[2], p[1])))
    panel = (
        '<div id="doc-review-panel">'
        '<b onclick="this.parentNode.classList.toggle(\'folded\')">'
        'review vs {} &middot; {} pages</b>'
        '<div class="doc-review-hint">'
        '<label><input type="checkbox" id="doc-review-toggle"> hide the marks</label>'
        '</div><ul>{}</ul></div>'
        '<script>(function(){{var b=document.body,t=document.getElementById("doc-review-toggle");'
        'if(localStorage.getItem("docReviewOff")==="1"){{b.classList.add("doc-review-off");t.checked=true;}}'
        't.onchange=function(){{b.classList.toggle("doc-review-off",t.checked);'
        'localStorage.setItem("docReviewOff",t.checked?"1":"0");}};}})();</script>'
    ).format(BASE, len(_pages), rows)
    return output.replace("</body>", _CSS + panel + "</body>")
