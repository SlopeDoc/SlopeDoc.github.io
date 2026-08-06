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
| `shader: plasma.frag` | single-pass fragment [shader](../../Primitives/Shader/basics) (optional `resolution: [w, h]`, `uniforms:`, `textures:`, see [below](#shader-items)) |
| `object: name` | C++-[registered object](../objects) or group |
| `mesh: bunny.obj` | mesh from an obj file (optional `smooth:`, `normalize:`; `at:` is a persistent transform label) |
| `camera: view_name` | camera view from `views/view_name.json` (`fly: true` for a flight transition) |
| `pause: 3` | [timed pause](../../presenter/pause) in seconds |
| `keyframe: label` | labels this frame for C++ updaters (see [keyframes](#keyframes)) |

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
    - step
    - latex: appears later     # space is reserved, earlier children
  at: column_handle            # never move (see stacks page)
  spacing: 0.02
  align: left                # left | center | right
```

!!! warning "Typos"
    Unknown keys are reported in the terminal instead of being silently ignored. If an item does not move where you expect, check the indentation: a field must be aligned with the first key after its item's dash.

### Shader items

A `shader:` item can declare its uniforms and its textures, which covers most of what a
single-pass shader needs without touching C++. Multi-pass, ping-pong and storage buffers
stay on the [C++ side](../../Primitives/Shader/advanced), since they need a streaming order
the manifest cannot express.

```yaml
- shader: sky.frag
  resolution: [900, 600]
  uniforms:
    sun:   [0.3, 0.9, 0.2]                  # vec3, type read off the literal
    tint:  "#ffcc88"                        # color
    steps: 64                               # int
    speed: {default: 1.0, min: 0, max: 5}   # bounded, so a slider
    mode:  {type: int, default: 0}          # explicit type
  textures:
    noise: noise.png
    grad:  {file: gradient.png, filter: nearest, wrap: repeat}
```

Each uniform becomes a persistent [tunable parameter](../../interactivity): it appears in
the Tuner panel while the shader is on screen, you drag it live, `Ctrl+S` saves it to
`views/params.json` and the next run picks it up. The shader follows it every frame.

Types are `float`, `int`, `bool`, `vec2`, `vec3` and `color` (vec4). The type is read off
the literal when it is unambiguous, and `type:` states it otherwise. Bounds are optional,
and a bounded parameter is drawn as a slider rather than a drag field.

Each texture binds an image file to the sampler of the same name, which the shader declares
itself:

```glsl
uniform sampler2D noise;
uniform vec2      noise_size;   // optional, its size in pixels
```

`filter` is `linear` (default) or `nearest`, `wrap` is `clamp` (default) or `repeat`. Only
image files here: a texture fed by another pass or by a previous frame stays in C++.

Both lists are re-read on every hot reload, so a uniform or a texture you delete from the
manifest really goes away instead of lingering from the previous load.

