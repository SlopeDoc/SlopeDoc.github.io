---
title: Code and algorithms
---

## Step by step code display

If you are doing computer science, algorithms and code is very often something you want to explain.
You can put a source file on a slide, syntax highlighted, and walk through it
line by line.

```c++
auto code = Code::FromFile("newton.py");
show << code->at("code") << code->reveal(START);
show << inNextFrame << code->reveal("loop") << code->focus("loop");
```

A file edited while the talk runs is re-read on
the next frame.

### Builders

!!! note "```c++ Code::FromFile(path file);``` — the whole file, language from its extension"
!!! note "```c++ Code::FromFile(path file, int first_line, int last_line);``` — a slice, 1-based, `last_line <= 0` for "to the end""
!!! note "```c++ Code::FromFile(path file, std::string begin_marker, std::string end_marker);``` — the span between two markers, markers excluded"
!!! note "```c++ Code::Add(std::string source, CodeLanguage lang = CodeLanguage::PlainText());``` — a string written in C++"

Each takes an optional trailing `CodeLanguage` to override what the extension
says: `CodeLanguage::ForName("python")`, `ForExtension("py")`.

## Named regions

A file can carry its own marks, in comments, so the deck names parts of the code
instead of counting lines:

```python
# slope:begin relax
for v in verts:
    v.p += step * force(v)
# slope:end relax
# slope:here done
```

`slope:begin` / `slope:end` name a **region**, `slope:here` a **point**. Marker
lines are stripped from what is shown, so the file stays runnable, and a region
survives edits above it.

## Revealing and focusing

```c++
show << code->reveal(START);                    // nothing written yet
show << inNextFrame << code->reveal("relax");   // types up to the end of the region
show << inNextFrame << code->focus("relax");    // dims everything else
show << inNextFrame << code->reveal(END) << code->unfocus();
```

| Cue | Takes |
| --- | --- |
| `reveal(START)` / `reveal(END)` | nothing, or all of it |
| `reveal("label")` | a point, or the end of a region |
| `reveal(line)` | a line of the code, 1-based |
| `focus("region")` | a named region |
| `focus("from", "to")` | the span between two labels |
| `focus(first, last)` | a line range |
| `unfocus()` | the whole code back at full opacity |







## Style

```c++
code->style.font         = Code::LoadFont("JetBrainsMono.ttf");
code->style.line_numbers = true;
code->style.font_scale   = 2.0f;
```

| Field | |
| --- | --- |
| `font` | any ttf, loaded once; falls back on `Options::CodeFont`, then polyscope's monospace |
| `font_scale` | on top of the slide state's own scale (default 2.2) |
| `tracking` | multiplies each glyph's advance, 1 keeps the font's metrics |
| `line_spacing` | 1.15 |
| `padding` | pixels around the block |
| `line_numbers` | off by default |
| `absolute_line_numbers` | numbers a slice by its lines in the file; `reveal` and `focus` stay relative to the loaded portion |
| `dim_factor` | how far the lines outside a focus are dimmed, 1 keeps them opaque |

Every colour is a [named parameter](../../live/params) — `code/text`,
`code/keyword`, `code/type`, `code/comment`, `code/literal`, `code/preproc`,
`code/function`, `code/constant`, `code/variable`, `code/operator`,
`code/line_number`, `code/highlight`, `code/background` — live in the Tuner and
saved like any other. Assigning a literal `Color` to one of the `style` links it to a previously defined color to set a common style.

## Languages

Highlighting comes from [tree-sitter](https://tree-sitter.github.io/).
**python, glsl, cpp and yaml** are built by default. As a deck is yaml, slope
can show its own decks. Changing or adding a grammar is set in cmake
variables, see [build](../../cmake#code-highlighting).

An unknown extension is drawn as plain text.

## Pseudocode

To explain an algorithm you often want pseudocode instead of source code,
written in the LaTeX. An `Algorithm`
is that environment, revealed and focused like the code above.

```c++
auto algo = Algorithm::FromFile("bfs.tex");
show << algo->at("pseudocode") << algo->focus("loop");
```

```latex
\begin{algorithmic}
\Procedure{BFS}{$G, s$}
  \State $Q \gets \{s\}$
  \While{$Q \neq \emptyset$} \slopemark{loop}
    \State $u \gets \Call{Pop}{Q}$ \Comment{oldest first}
    \For{$v \in N(u) \setminus \mathrm{seen}$} \slopemark{relax}
      \State \Call{Push}{$Q, v$}
    \EndFor \slopemark{relaxed}
  \EndWhile
\EndProcedure
\end{algorithmic}
```

!!! note "```c++ Algorithm::FromFile(path file, scalar scale = 1, int width = -1);``` — a `.tex` holding the environment"
!!! note "```c++ Algorithm::Add(TexObject tex, scalar scale = 1, int width = -1);``` — the same written in C++"



### Marks instead of regions

`\slopemark{name}` names the line it sits on, and the
[cues](#revealing-and-focusing) take those names. `focus("relax")` is the line of
one mark, `focus("relax", "relaxed")` the span between two.





## Deck format

```yaml
- code: newton.py         # the file, relative to the data path
  id: newton
  at: source              # placement, defaults to a label from the filename
  lines: [12, 40]         # a slice, 1-based
  language: python        # overrides the extension
  line_numbers: absolute  # true | false | absolute | relative
  font: JetBrainsMono.ttf
  font_scale: 2.0
  tracking: 1.0
  line_spacing: 1.15
  padding: 12
  dim: 0.35               # style.dim_factor

- step
- set: newton             # the code stays where it is
  reveal: relax           # START, END, a label, or a line number
  focus: relax            # a region, [label, label], [first, last], or null
```



Pseudocode is an `algo:` item, with the same keys:

```yaml
- algo: bfs.tex           # the file, relative to the data path
  id: bfs
  at: pseudocode          # defaults to a label from the filename
  scale: 1.0
  width: 300              # pt
  dim: 0.35

- step
- set: bfs
  focus: loop             # a mark, [from, to], [first, last], or null
  reveal: relax           # START, END, a mark, or a line number
```

The content of the `.tex` is part of the primitive's identity, so editing it
while the talk runs recompiles it in place.
