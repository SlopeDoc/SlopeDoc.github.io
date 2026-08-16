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

Every primitive that can be written in a manifest documents its own keys, in a
**Manifest format** section on its own page.

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
- image: fig.png
  below: my_key           # below/above/right_of/left_of another item
  padding: 0.05
- formula: p
  follow: fx.center       # rides a moving point instead of a fixed position
  offset: [0.025, -0.03]
```

When omitted, `load`/`image` items default to a label derived from their key or filename, so everything is drag-editable out of the box.

`follow:` places an item on a moving value: a point of the 3D scene, of the screen, or of a shader's world space, see [tracking](../../placement/tracking#manifest-format).

### State

Any screen item also takes the fields the slide *state* carries. They are not
part of the primitive, they describe this placement of it:

```yaml
- image: fig.png
  at: fig
  alpha: 0.5              # opacity
  rot: 20                 # rotation, in degrees
  zoom: 1.5               # scales this placement
```

??? note "`zoom` and `scale` are different things"
    `scale` (on `image`, `gif`, `video`, `latex`) is how big the primitive
    itself is, its default size. `zoom` scales one placement of it, and animates.

### Steps

A bare `- step` marker splits a frame into clicks (the equivalent of `inNextFrame`): every item after it appears on the next click.

```yaml
- frame:
    - load: question
    - step
    - load: answer
      below: question
```

### Keyframes

A `keyframe:` labels the frame it appears in, so C++ [updaters](../../Primitives/Animation) can branch on `t.afterKeyframe("label")` (also `atKeyframe`, `beforeKeyframe`) instead of counting frames: the test follows the label wherever manifest edits move it.

```yaml
- load: usual_pipeline
- step
- keyframe: pipeline_shown
- load: reconstruct
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

After a `- step` (or in a later frame), existing items can be manipulated:

```yaml
- step
- remove: [isurf, side_notes]     # item ids or groups
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
