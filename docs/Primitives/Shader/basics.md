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

!!! tip "Unknown names never throw"
    A uniform the shader doesn't currently declare is silently ignored rather than thrown, so you can  exactly what you want while editing the shader live and adding/removing uniforms as you go.

## Sharing code with `#include`

```glsl
#include "sdf.glsl"       // next to the including file, else the project data path
#include <palette.glsl>   // the shader stdlib
```

Plain textual inclusion, expanded before the source ever reaches the GL compiler. You can use `#pragma once`, and include cycles are refused.

