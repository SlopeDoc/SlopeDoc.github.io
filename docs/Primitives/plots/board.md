---
title: Board
---

When talking about math, it's hard to dodge function plots, when talking about results it's hard to dodge curves, so write them on a board!

```c++
show << Board::Add("fig", vec2(-M_PI, M_PI), vec2(-1.2, 1.2))->at("figure")
     << inNextFrame
     << Plot::Add("sine", "fig", [](scalar x){ return std::sin(x); })
     << Legend::Add("fig");
```

| Primitive | |
| --- | --- |
| `Board` | the frame: background, data rectangle, grid, axes, tick labels. No data of its own |
| [`Plot`](../plot) | one curve, drawn in the rectangle of the board it names |
| [`Scatter`](../scatter) | the measurements themselves, as marks |
| `Legend` | what the curves of a board are called, in one of its corners |

Each plot primitive is independent so you can make them appear and disappear when you want. You can edit each primitive shader to customize the look.

## Adding one

!!! note "```c++ Board::Add(std::string name, optional<vec2> x, optional<vec2> y, int w = 1100, int h = 620);```"
    A range given here is fixed; omitted, it is a tunable parameter. `w` and `h`
    are the render resolution of the frame.

A board is known by its name. `Plot::Add("sine", "fig", f)` takes the board or
that name. Use `setRange(x, y)` to change the view.

## What it publishes

Everything the board is made of is published under its name:

| Setting | | Default |
| --- | --- | --- |
| `fig/xrange` `fig/yrange` | the data interval across and up | (-1, 1) |
| `fig/xscale` `fig/yscale` | `linear` or `log` | linear |
| `fig/xstep` `fig/ystep` | data units between ticks, 0 for round numbers from the range | 0 |
| `fig/tick_font` | `latex` or `text` | latex |
| `fig/tick_size` | how big the tick labels are | 0.4 |
| `fig/xticks` | which edge carries the labels: `bottom` `top` `none` | bottom |
| `fig/yticks` | `left` `right` `none` | left |
| `fig/show_grid` `fig/show_axes` `fig/show_frame` | the grid, the lines x = 0 and y = 0, the border | true |
| `fig/background` `fig/grid` `fig/axis` | the rectangle, the grid lines, the axes and labels | white |
| `fig/line_width` | pixels, the frame and axis weight | 1.8 |

Latex ticks cost a compile per label, so a range that moves every frame wants
`tick_font: text`.

## Axis names and labels

For the sake of simplicity, you must add axis names by hand, as standard text.
You may use `label(primitive, at)` to follow a point in the data space.

!!! note "```c++ Board::label(ScreenPrimitivePtr p, vec2 at, vec2 offset = vec2::Zero());```"
    `at` is in data units, on a log axis too. `offset` is added afterwards in
    screen units, to clear the point itself.

```c++
show << fig->label(Formula::Add("\\varepsilon_{20}"), vec2(20, 1e-4), vec2(-0.03, 0));
```

The point is resolved every frame, so the label follows the view: `setRange`, or a
snippet owning `fig/xrange`, moves it.

From a deck, `follow:` places anything at a point of the board:

```yaml
- formula: \varepsilon_{20}
  follow: conv.last     # a snippet section returning a point of the board
  offset: [-0.05, 0]
```









## Setting a value

Every name a board, a curve or a legend publishes is settable three ways, in
this order of priority:

| | |
| --- | --- |
| a [snippet](../../../live/snippets) section of that name | drives it, never a parameter |
| a deck key, or `settings.set` from C++ | fixes it, never a parameter |
| neither | a [parameter](../../../live/params), tunable in the Tuner and saved |

```lua
--- fig/xrange
-- the view, and its motion, owned by the snippet
return vec2(-3.15 + 3.75 * t:sinceKeyframe("zoom"), 3.15)
```

```c++
fig->settings.set("xticks", "right");   // fixed, gone from the Tuner
```

## The legend

`Legend::Add("fig")` lists the curves and scatters of that board, in the order
they were declared, each drawing its own swatch, under its `caption` or else its
name. It publishes under `fig_legend/`:

| Setting | | Default |
| --- | --- | --- |
| `fig_legend/corner` | `top_left` `top_right` `bottom_left` `bottom_right` | top_right |
| `fig_legend/text_size` | how big the captions are | 0.4 |
| `fig_legend/swatch` | length of a swatch, in pixels | 46 |
| `fig_legend/padding` | the space around and between | 12 |
| `fig_legend/background` `fig_legend/border` `fig_legend/text` | the box, its edge, the captions | |

## The shader is a file you edit

A board and a curve *are* [shaders](../../Shader/basics). The first time one is
shown, its fragment program is written to `views/<name>.glsl` and drawn from
there, hot-reloaded like any other. Open the file mid-talk and the figure
changes as you save. Delete it and the default comes back.

The uniforms are bound already, named after the settings above. A board gets
`background`, `grid_color`, `axis_color`, `grid_step`, `axis_at` (where x = 0 and
y = 0 fall), `line_width` and `show` (grid, axes, frame), and draws in the
board's data space, read as `iWorld()`. What a curve gets, and an example of
editing one, is on the [curves](../plot#its-shader) page.

## Deck format

```yaml
- board: fig            # the frame
  at: figure            # placement, defaults to the board's name
  resolution: [1100, 620]
  yrange: [-1.35, 1.35] # xrange left out: a parameter, or owned by a snippet
  tick_font: text       # any setting of the table above

- legend: fig           # the legend of the board "fig"
  corner: bottom_left
```

A [plot](../plot#deck-format) and a [scatter](../scatter#deck-format) name their
board with `board:`, or take the last one declared above them.
