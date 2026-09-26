---
title: Deck format
---

## Deck format

A deck is a list of frames, each frame a list of *items*:

```yaml
slides:
  - frame:
      - title: First slide
      - ...
  - frame:
      - ...
    same_title: true      # keep the previous frame's title
```

### Content items

Every primitive that can be written in a deck documents its own keys, in a
**Deck format** section on its own page.

The keys on this page are the ones that belong to the deck itself rather than to
any one primitive: placement, steps, keyframes, ids and groups, and operations.

### Placement

Screen items take one placement key:

```yaml
- load: my_key
  at: my_label            # persistent, drag-editable label
- formula: x^2
  at: [0.5, 0.4]          # fixed position
- latex: some text
  at: TOP                 # TOP | CENTER | BOTTOM
- image: logo.png
  at: BOTTOM_RIGHT        # flush to an edge or a corner
  offset: [0, -0.05]      # shifts any placed item, so items can share a label
- image: fig.png
  below: my_key           # below/above/right_of/left_of another item
  padding: 0.05
- formula: p
  follow: fx.center       # follows a moving point instead of a fixed position
  offset: [0.025, -0.03]
```

`TOP_LEFT`, `TOP_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_RIGHT`, `LEFT` and `RIGHT` sit
the item against that edge of the window, `config: margin` away. The item's own
size is taken into account, so a logo and a caption are both flush with it.

When omitted, `load`/`image` items default to a label derived from their key or filename, so everything is drag-editable by default.

`follow:` places an item on a moving value: a point of the 3D scene, of the screen, or of a shader's world space, see [tracking](../../placement/tracking#deck-format).

### State

Any screen item also takes the fields the slide *state* carries. They are not
part of the primitive, they describe this placement of it:

```yaml
- image: fig.png
  at: fig
  alpha: 0.5              # opacity
  rot: 20                 # rotation, in degrees
  zoom: 1.5               # scales this placement
  depth: 1                # drawn above lower depths, 0 by default
```

??? note "`zoom` and `scale` are different things"
    `scale` (on `image`, `gif`, `video`, `latex`) is how big the primitive
    itself is, its default size. `zoom` scales one placement of it, and animates.

### Steps

A `- step` line splits a frame into clicks, like `inNextFrame` in C++. Every item after it appears on the next click.

```yaml
- frame:
    - load: question
    - step
    - load: answer
      below: question
```

### Keyframes

A `keyframe:` labels the frame it appears in, so C++ [updaters](../../Primitives/Animation) can branch on `t.afterKeyframe("label")` (also `atKeyframe`, `beforeKeyframe`) instead of counting frames: the test follows the label wherever deck edits move it.

```yaml
- load: usual_pipeline
- step
- keyframe: pipeline_shown
- load: reconstruct
```

### A template on every frame

`template:`, beside `slides:`, holds the items every frame gets, drawn behind its own. A frame excludes it with `no_template`.

```yaml
template:
  - latex: \color{gray} My talk
    at: footer
slides:
  - frame:
      - title: First slide
  - frame:
      - title: A frame without the footer
    no_template: true
```

It is built once and the same primitives are re-used, so a footer stays in place across a slide change instead of cross-fading with itself. It cannot contain a `- step`.

### Named groups

Any other top-level list is a group of items (or `params:` and `items:`), expanded wherever its name appears in a frame:

```yaml
axes:
  params: {label: x}      # an empty default must be given at each call
  items:
    - object: grid
    - latex: $label
      at: x_label
slides:
  - frame:
      - axes              # the defaults
      - object: curve
  - frame:
      - axes: time_axes   # a call, its arguments beside it
        label: t
      - object: other_curve
```

`$name` is replaced by the argument as it is (a number, a list, a text), `${name}` inside a text, and `${id}` is the id of the call. A group can contain `- step`.

### Background

`background:` sets the [background color](../../Primitives/colors#background) from that frame on:

```yaml
- background: bg              # a named color
- background: [0.05, 0.05, 0.08]
```

### Referencing items : ids and groups

Operations refer to items by their key (latex key, image filename stem, object name, `title`), or an explicit `id:`. An `id:` names a primitive like a variable in C++, so two items written the same way without one are two primitives. Any item can also join a tagged group with `group: name`. A group has no position of its own, operations simply map over its members.

```yaml
- formula: \mathcal{S}
  id: isurf
- latex: a remark
  group: side_notes
```

### Operations

After a `- step` (or in a later frame), existing items can be manipulated:

```yaml
- step
- remove: [old_fig, side_notes]   # item ids or groups, or a group call's id
- isurf                           # shows it again, where it was last placed
- replace: fig
  with: {image: better_fig.png}
- set: isurf                      # re-place an existing item,
  at: new_label                   # transition animated
- set: fig                        # or restyle it without moving it,
  alpha: 0.3                      # any of the state fields above
  rot: -20
```

!!! warning "Typos"
    Unknown keys are reported in the terminal instead of being silently ignored. If an item does not move where you expect, check the indentation: a field must be aligned with the first key after its item's dash.
