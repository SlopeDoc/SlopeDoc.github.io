---
title: Getting started
---

## The deck system

Recompiling to move a formula gets old fast. The deck system splits a presentation in two:

- **composition** (which content, on which slide, at which position) lives in a `deck.yaml` manifest, **hot-reloaded** while the presentation runs;
- **behavior** (updaters, computed meshes, anything that needs real code) stays in C++ and is exposed to the manifest by *registering objects*.

Editing the manifest, a latex definition, or a saved camera while the show runs recomposes the slides in place: you keep your current slide, primitives keep their state, and compiled latex or loaded textures are reused.

### A minimal deck project

```c++
#include "slope.h"

using namespace slope;

DeckLoader deck;

int main(int argc, char** argv) {
    deck.init("my_talk", "deck.yaml", argc, argv);

    // C++-defined content, referenced by name in the manifest
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
      - step:
          - load: my_key        # content from latex.json
```

`init` also loads the project's `latex.json` (latex definitions, see [dynamic latex](../../Primitives/Latex/dynamic)) and `commands.tex` (latex preamble) when they exist — both hot-reloaded too. Custom paths can be given at the top of the manifest with the `latex:` and `commands:` keys.

### What hot reload watches

| File | Effect when edited |
| --- | --- |
| `deck.yaml` | slides are recomposed in place |
| `latex.json` | edited entries are recompiled |
| `commands.tex` | preamble change, every formula is recompiled |
| saved camera views | the view is reloaded |
| `views/params.json` | [tunable parameters](../../interactivity) are updated |

A parse error in the manifest is printed to the terminal and the previous composition stays on screen.

Next: the full [manifest format](../manifest), and [registering C++ objects](../objects).
