---
title: In-app editor
---

## Editing a file without changing window

Everything slope hot-reloads is a text file, and `E` opens an editor on those
files inside the running presentation. You can correct a shader, retype a line of
pseudocode or add a slide to the deck, wtithout a text-editor.

The list on the left is every watched file: the deck, the latex definitions and
preamble, [Lua snippets](../snippets), [shader](../../Primitives/Shader/basics)
sources and their includes, and the files shown as
[code or pseudocode](../../Primitives/code).

The editor only writes to disk. The same file watch used for an external editor
reads the change on the next frame, so saving is what reloads.

### Keys

| Key | Action |
| --- | --- |
| `E` | open and close the editor |
| `Ctrl` + `S` | save the open file, which reloads it |
| `Ctrl` + `/` | comment or uncomment the selected lines, in the language of the file |
| `Tab` | indent, two spaces in a yaml file |
| `Enter` | a new line, indented like the one it ends |
| `Ctrl` + `C` / `X` / `V` | copy, cut, paste |
| `Escape` | leave the text field, then close the window |

The `size` slider scales the editor font. Syntax highlighting is the one a
[code primitive](../../Primitives/code#languages) uses, and covers the same languages.

### Files that do not exist yet

A file a deck names but that does not exist is shown greyed out in the list, with
a **Create file** button. Write `shader: new.glsl` in the deck, then create the
file from the list.
