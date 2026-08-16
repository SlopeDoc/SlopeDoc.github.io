---
title: Basics
---

<video src="../../../static/shader1.mp4" muted autoplay loop controls width="100%" >
</video>

You need to express something that would require control over litteraly every pixel of the screen? Do it with a shader!

Slope offers ShaderToy style shaders, and basics of GPU compute, that are all hot-reloaded!

=== "C++"

    ```c++ title="main.cpp"
    #include "slope.h"
    using namespace slope;

    Slideshow show;

    int main(int argc, char** argv) {
        show.init("shader_demo", argc, argv);
        show << Shader::FromFile("plasma.frag")->at(CENTER);
        show.run();
        return 0;
    }
    ```

=== "Deck manifest"
    Only pure fragment shaders can be created in deck manifests.

    ```yaml title="deck.yaml"
    slides:
      - frame:
          - shader: plasma.frag
            at: screen
    ```

```glsl title="plasma.frag"
void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    float v = sin(uv.x * 10.0 + iTime)
            + sin(uv.y * 10.0 + iTime * 1.3)
            + sin((uv.x + uv.y) * 10.0 + iTime * 0.7)
            + sin(length(uv - 0.5) * 20.0 - iTime * 2.0);
    fragColor = vec4(0.5 + 0.5 * sin(v * 1.5707 + vec3(0.0, 2.0, 4.0)), 1.0);
}
```


## Writing the shader itself

A plain `.frag` file with no `#version` line gets a prelude prepended, declaring the render target, the input state and an output. If you specify your own `#version` then nothing is added in your shaders (no uniforms neither).

| Uniform | Type | Meaning |
| --- | --- | --- |
| `iResolution` | vec2 | render target size, pixels |
| `iAspect` | float | `iResolution.x / iResolution.y` |
| `iTime` | float | seconds since the primitive appeared |
| `iTimeDelta` | float | seconds since last frame |
| `iFrame` | int | frames this shader has rendered |
| `iFrameRate` | float | frames per second, smoothed |
| `iMouse` | vec4 | xy = cursor (px, y up); zw = last click, z<0 while unpressed |
| `iMouseNorm` | vec2 | cursor in 0..1 across the rect, y up |
| `iHovered` | float | 1.0 while the cursor is over the rect |
| `iDate` | vec4 | year, month(1-12), day, seconds since midnight |
| `fragColor` | out vec4 | write your result here |

An even smaller one, if all you want is to see the built-ins move:

## Following the talk

Like all primitives, shaders also have updaters that get TimeObjects! Even better, the content of a TimeObject is passed to the shaders as uniforms. So you can build shaders that smoothly adapt to your talk!

| Uniform | Meaning |
| --- | --- |
| `from_begin` | seconds since the slideshow started |
| `from_action` | seconds since the last slide change |
| `inner_time` | = `iTime` |
| `delta_time` | = `iTimeDelta` |
| `absolute_frame_number` | current slide index in the deck |
| `relative_frame_number` | slides since this shader appeared |
| `transition_parameter` | 0 → 1 across the intro/outro |

A keyframe branch or an ease is written in a [snippet](../../../live/snippets) and read as a uniform, see [uniforms by name](#a-uniform-fed-by-a-value-that-already-exists).

## How to declare your own Uniforms

Declare `uniform float radius;` in the shader, then from C++ push a fixed value:

```c++
fx->set("radius", 0.3f);
```

or bind it to something live, re-read every frame:

```c++
fx->bind("radius", [&]{ return slider_value; });
```

`set`/`bind` accept `float`, `int`, `vec2`, `vec` (vec3) and `RGBA` (vec4).

`bind` also takes a **name on its own**, feeding the uniform from the [parameter or snippet variable](../../../live/snippets) of that name, with no lambda and no C++ owner:

```c++
fx->bind("reveal");                          // uniform <- the value called "reveal"
fx->bind({"show_field", "show_basin"});      // several at once
```

The width follows the value, 1 to 4 components, so one call serves a `float` and a `vec3`. Same mechanism as a bare name in a manifest, below.

!!! tip "Unknown names never throw"
    A uniform the shader doesn't currently declare is silently ignored rather than thrown, so you can  exactly what you want while editing the shader live and adding/removing uniforms as you go.

## Sharing code with `#include`

```glsl
#include "sdf.glsl"       // next to the including file, else the project data path
#include <palette.glsl>   // the shader stdlib
```

Plain textual inclusion, expanded before the source ever reaches the GL compiler. You can use `#pragma once`, and include cycles are refused.


## Manifest format

A `shader:` item in a [deck manifest](../../../deck/manifest) declares what goes *into* the
shader: its uniforms, its textures, and the region of the plane it draws. That covers most of
what a single-pass shader needs without touching C++. Multi-pass, ping-pong and storage
buffers need a streaming order the manifest cannot express, and stay on the
[C++ side](../advanced).

```yaml
- shader: sky.frag
  resolution: [900, 600]
  uniforms:
    sun:      dir                                       # a type name on its own
    steps:    {type: int, default: 64}                  # long form, with a default
    tint:     {type: color, default: "#ffcc88"}
    speed:    {type: float, default: 1.0, min: 0, max: 5}   # bounded, so a slider
    controls: "vec3[8]"                                 # an array
  textures:
    noise: noise.png
    grad:  {file: gradient.png, filter: nearest, wrap: repeat}
```

Each uniform **declared with a type** becomes a persistent [tunable parameter](../../../live/params): it appears in
the Tuner panel while the shader is on screen, you drag it live, `Ctrl+S` saves it to
`views/params.json` and the next run picks it up. The shader follows it every frame. An entry
with no type declares nothing and reads an existing value instead, below.

Types are `float`, `int`, `bool`, `vec2`, `vec3`, `dir` and `color` (vec4). A `dir` is a
unit vector, aimed on a ball rather than typed component by component. Bounds are
optional, and a bounded parameter is drawn as a slider rather than a drag field.

`<type>[N]` declares an array, from 1 to 64 elements. The shader sees
`uniform vec3 controls[8];` and the panel shows one parameter per element, named
`controls[0]` to `controls[7]`, each with its own handle. Its `default` is a list of one
value per element. Watch the quotes: inside a flow mapping yaml reads the brackets itself,
so write `{type: "vec3[8]", default: [...]}`.

Each texture binds an image file to the sampler of the same name, which the shader declares
itself:

```glsl
uniform sampler2D noise;
uniform vec2      noise_size;   // optional, its size in pixels
```

`filter` is `linear` (default) or `nearest`, `wrap` is `clamp` (default) or `repeat`. Only
image files here: a texture fed by another pass or by a previous frame stays in C++.

### A uniform fed by a value that already exists

A list entry with **no type** declares nothing: the uniform is fed by the [snippet
variable](../../../live/snippets) or [parameter](../../../live/params) of that name, which is
how a value computed elsewhere reaches a shader with nothing in between:

```yaml
- shader: field.frag
  id: fx
  uniforms:
    - center                   # a snippet variable, or a parameter, already declared
    - radius
    speed: {type: float, default: 1.0, max: 5}   # the typed form still applies
```

### `view` : the shader's world space

`view:` says which region of the plane the shader draws, which makes its pixels addressable
from outside:

```yaml
- shader: field.frag
  view: {half: 4}                       # half the height it shows, in world units
- shader: other.frag
  view: {center: [1, 0], half: zoom}    # a fixed center, and a half-height read live
```

`view: 4` on its own is `{half: 4}`, centered on the origin. `half` and `center` can each be
a snippet or parameter name instead of a number, so the framing can animate.

A label can then be placed on a point *of that space*, with `tracker` or `follow:` on the
[tracking page](../../../placement/tracking#following-a-point-of-a-shader), and it lands on
what the shader draws for that value. Without a `view:` a shader has no world points.

### On a shader registered from C++

All three keys also apply to an `object:` naming a shader, so a shader that needed C++ for
its updater does not lose the declarative layer with it:

```yaml
- object: field
  view: {half: 2}
  uniforms:
    - reveal
```

Its parameters are named after the object, not the item's `id:`, so they hold however many
slides show it, and a hot reload drops only what the manifest declared last time, leaving its
C++ owner's own binds standing. Declaring these keys on more than one item is reported, and
an `object:` that is a group, or not a shader, refuses them.
