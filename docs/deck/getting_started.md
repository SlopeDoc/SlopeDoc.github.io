---
title: Getting started
---

## The deck system

While you can build all your slides in pure C++, you have to recompile each time you want to see an update.
This can be frustrating for simply slide creation like text, math and images. To avoid this, you can instead build your presentation
fully interactivly without having to recompile most of the time.

The deck system splits a presentation in two:

- **composition** (which content, on which slide, at which position) lives in a `deck.yaml` manifest, **hot-reloaded** while the presentation runs;
- **behavior** (updaters, computed meshes, anything that needs real code) stays in C++ and is exposed to the manifest by *registering objects*.

Editing the manifest, a latex definition, or a saved camera while the show runs recomposes the slides in place.

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
          - load: my_key        # content from the latex definitions file
```

`init` also loads a latex definitions file (see [dynamic latex](../../Primitives/Latex/dynamic)) and a latex preamble — both hot-reloaded too. Their paths are given at the top of the manifest with the `latex:` and `commands:` keys; when omitted, the project's `latex.json` and `commands.tex` are used if they exist.

```yaml
latex: my_definitions.json
commands: my_preamble.tex
slides:
  - ...
```

### What hot reload watches

| File | Effect when edited |
| --- | --- |
| `deck.yaml` | slides are recomposed in place |
| latex definitions file | edited entries are recompiled |
| latex preamble file | every formula is recompiled |
| saved camera views | the view is reloaded |
| `views/params.json` | [tunable parameters](../../interactivity) are updated |

A parse error in the manifest is printed to the terminal and the previous composition stays on screen.

Next: the full [manifest format](../manifest), and [registering C++ objects](../objects).
