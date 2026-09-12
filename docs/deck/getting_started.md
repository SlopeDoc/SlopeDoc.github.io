---
title: Getting started
---

## The deck system

While you can build all your slides in pure C++, you have to recompile each time you want to see an update.
This can be frustrating for simple slide creation like text, math and images. To avoid this, you can instead build your presentation
fully interactively without having to recompile most of the time.

The deck system splits a presentation in three, by how often you edit each part:

- **composition** (which content, on which slide, at which position) lives in a `deck.yaml` file, **hot-reloaded** while the presentation runs;
- **what it animates on** lives next to it: [tunable parameters](../../live/params) for the constants, [Lua snippets](../../live/snippets) for the logic, both re-read on save;
- **computation** (meshes, solves, simulation steps) stays in C++ and is exposed to the deck by *registering objects*.

Only the last costs a rebuild. Editing the deck, a snippet, a latex definition or a saved camera takes effect on the next frame.

### A minimal deck project

```c++
#include "slope.h"

using namespace slope;

DeckLoader deck;

int main(int argc, char** argv) {
    deck.init("my_talk", "deck.yaml", argc, argv);

    // C++-defined content, referenced by name in the deck
    deck.registerObject("spot", [](){ return Mesh::Add("spot.obj"); });

    deck.run();
    return 0;
}
```

with next to it a `deck.yaml`:

```yaml
slides:
  - frame:
      - title: My talk
      - latex: it starts \emph{here}
        at: [0.5, 0.6]
  - frame:
      - title: A mesh, from C++
      - object: spot
      - step
      - load: my_key        # content from the latex definitions file
```

`init` also loads a latex definitions file (see [dynamic latex](../../Primitives/Latex/dynamic)) and a latex preamble, both hot-reloaded too. Their paths are given at the top of the deck with the `latex:` and `commands:` keys; when omitted, the project's `latex.json` and `commands.tex` are used if they exist. `snippets:` names the [Lua files](../../live/snippets) the deck animates with, one or several.

```yaml
latex: my_definitions.json
commands: my_preamble.tex
snippets: snippets.lua
slides:
  - ...
```

 `preamble:` is latex written
straight in the deck, a string or a list of lines, added on top of
`commands.tex` and hot-reloaded with everything else.

```yaml
preamble:
  - \usepackage{libertine}
```

### Deck settings

`config:` sets the values used in all frames (like title size, etc...). 

```yaml
config:
  title_scale: 1.5        # scale of title items
  latex_scale: 1.0        # default scale of latex, formula and algo items
  box_roundness: 1.0      # corner radius of boxes
  margin: 0.06            # gap the edge anchors leave, one number or [x, y]
  top: [0.5, 0.1]         # where at: TOP puts an item
  center: [0.5, 0.5]
  bottom: [0.5, 0.9]
```

### What hot reload watches

| File | Effect when edited |
| --- | --- |
| `deck.yaml` | slides are recomposed in place |
| `preamble:` or `config:` in the deck | the same, formulas recompiled if the preamble moved |
| latex definitions file | edited entries are recompiled, and the slides recomposed |
| latex preamble file | every formula is recompiled |
| saved camera views | the view is reloaded |
| `views/params.json` | [tunable parameters](../../live/params) are updated |
| a [snippet](../../live/snippets) file | the sections are re-read, and the next frame animates with them |

Next: the full [deck format](../deck_format), and [registering C++ objects](../objects).
