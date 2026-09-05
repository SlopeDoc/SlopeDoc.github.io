---
title: Curves
---

A curve is its own primitive, drawn over the rectangle of its [board](../board).

```c++
show << Plot::Add("sine", "fig", [](scalar x){ return std::sin(x); });
```

## Sources

!!! note "```c++ Plot::Add(name, board, ...)```"
    ```c++
    Plot::Add("f",   fig, [](scalar x){ return x*x; });   // a C++ callable
    Plot::Add("res", fig, "residuals.csv");               // two columns
    Plot::Add("pts", fig, points);                        // vector<vec2>
    Plot::Add("y",   fig, ys, vec2(0, 10));               // values on a grid
    Plot::FromSnippet("lua", fig, "profile");             // a Lua section
    ```

A callable and a [Lua section](../../../live/snippets) are sampled over the
board's x range (possibly time-dependent). A csv is re-read when it is saved, so a figure updates while the experiment
runs.



## What it publishes

| Setting | | Default |
| --- | --- | --- |
| `sine/color` | the ink | next in the board's palette |
| `sine/width` | stroke width in pixels | 3 |
| `sine/reveal` | how much of it is drawn, 0 to 1 | 1 |



`caption` is what a [legend](../board#the-legend) calls the curve when its name
is not what a reader wants.

## Its shader

A curve's fragment program is written to `views/<name>.glsl` the first time it
is shown, and drawn from there, see [the board's
page](../board#the-shader-is-a-file-you-edit). It gets its samples as `samples`
with the `span` they cover, plus `color`, `line_width` and `reveal`.

`#include <plot.glsl>` carries what a curve in data coordinates needs, see the
[shader stdlib](../../Shader/stdlib). Example for a dashed curve:

```glsl
#include <plot.glsl>
uniform sampler2D samples;
uniform vec2  span;
uniform vec4  color;
uniform float line_width, reveal;

void main() {
    vec2 px = iPixelXY(), p = iWorld();
    float d = sdGraph(p, dataAt(samples, span, p.x),
                         dataSlope(samples, span, p.x), px);
    float a = color.a * stroke(d, line_width)
            * dashMask(p, vec2(9.0, 6.0), px)      // mark, gap, in pixels
            * inSpan(p.x, span, px.x)
            * revealMask(p.x, span, reveal, px.x);
    fragColor = vec4(color.rgb, a);
}
```

## Deck format

```yaml
- plot: sine            # "board: fig" implied, the last board declared
  snippet: sine         # one source: snippet, data, values, points
  color: "#2f7fd1"
  width: 4
  caption: $\sin x$
```

A formula is a function snippet. `data:` is a csv of two
columns, `points:` a list of `[x, y]`, `values:` a list of numbers over an
optional `span: [min, max]`.
