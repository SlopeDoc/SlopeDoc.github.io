---
title: Scatter
---

A simple scatter plot, over a [board](../board).

```c++
show << Board::Add("conv")->at("figure")
     << Scatter::Add("points", "conv", "residuals.csv");
```

## Sources

!!! note "```c++ Scatter::Add(name, board, ...)```"
    ```c++
    Scatter::Add("s", fig, points);            // vector<vec2>
    Scatter::Add("s", fig, "residuals.csv");   // two columns, re-read on save
    Scatter::Add("s", fig, ys, vec2(0, 10));   // values on a grid
    ```

A point outside the range is not drawn.

## What it publishes

| Setting | | Default |
| --- | --- | --- |
| `s/color` | the ink | next in the board's palette |
| `s/size` | radius of a mark, in pixels | 5 |
| `s/reveal` | how much of it is there, 0 to 1 | 1 |

Like a curve it arrives left to right, and `caption` is what a
[legend](../board#the-legend) calls it. Setting one of these names is the same
[three ways](../board#setting-a-value) as everywhere else.

Marks are drawn over the board with ImGui, so a scatter carries no shader and
writes no `views/*.glsl` file.

## Deck format

```yaml
- scatter: samples      # "board: conv" implied, the last board declared
  data: residuals.csv   # one source: data, values, points
  size: 6
  caption: measured
```
