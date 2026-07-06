---
title: Manifest format
---

## Manifest format

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

| Item | Content |
| --- | --- |
| `title: text` | slide title |
| `load: key` | latex content from the [definitions file](../getting_started) (text/formula mode comes from the entry) |
| `latex: \emph{inline} latex` | inline text-mode latex |
| `formula: e^{i\pi}+1=0` | inline math-mode latex |
| `image: figure.png` | image (optional `scale:`) |
| `object: name` | C++-[registered object](../objects) or group |
| `mesh: bunny.obj` | mesh from an obj file (optional `smooth:`, `normalize:`; `at:` is a persistent transform label) |
| `camera: view_name` | camera view from `views/view_name.json` (`fly: true` for a flight transition) |
| `pause: 3` | [timed pause](../../presenter/pause) in seconds |

### Placement

Screen items take one placement key:

```yaml
- load: my_key
  at: my_label            # persistent, drag-editable label
- formula: x^2
  at: [0.5, 0.4]          # fixed position
- latex: some text
  at: TOP                 # TOP | CENTER | BOTTOM
- image: fig.png
  below: my_key           # below/above/right_of/left_of another item
  padding: 0.05
```

When omitted, `load`/`image` items default to a label derived from their key or filename, so everything is drag-editable out of the box.

### Steps

A `step:` reveals its items on the next click, inside the same frame (the equivalent of `inNextFrame`):

```yaml
- frame:
    - load: question
    - step:
        - load: answer
          below: question
```

### Referencing items : ids and groups

Operations refer to items by their key (latex key, image filename stem, object name, `title`), or an explicit `id:`. Any item can also join a tagged group with `group: name`; a group has no position of its own, operations simply map over its members.

```yaml
- formula: \mathcal{S}
  id: isurf
- latex: a remark
  group: side_notes
```

### Operations

Inside a `step:` (or a later frame), existing items can be manipulated:

```yaml
- step:
    - remove: [isurf, side_notes]     # item ids or groups
    - replace: fig
      with: {image: better_fig.png}
    - set: isurf                      # re-place an existing item,
      at: new_label                   # transition animated
    - move: side_notes                # offset a group (or an item),
      by: [0.1, -0.05]                # composed on top of placements
```

### Connectors and layout

```yaml
- arrow: {from: KR2, to: KR2_sub, bend: 0.25, color: "#aa0000"}
```

Arrow endpoints follow their target every frame: an item id, a `[x,y]` position, or a label. `from_offset` / `to_offset` shift the attach points (see [shapes & arrows](../../Primitives/shapes)).

```yaml
- box:                       # rectangle englobing its items, following them
    - latex: framed content
    - image: fig.png
  padding: 0.02              # also padx/pady, color, thickness,
  filled: true               # filled, fill_color, alpha, id

- stack:                     # children laid out below one another
    - latex: first paragraph
    - step:
        - latex: appears later    # space is reserved, earlier children
  at: column_handle               # never move (see stacks page)
  spacing: 0.02
  align: left                # left | center | right
```

!!! warning "Typos"
    Unknown keys are reported in the terminal instead of being silently ignored — if an item does not move where you expect, check the indentation: a field must be aligned with the first key after its item's dash.
