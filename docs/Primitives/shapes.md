---
title: Shapes & arrows
---

## 2D vector graphics

Live vector shapes, drawn every frame: resolution independent, animatable, with a *draw-on* intro (the stroke grows along its arc length).

```c++
auto circle = Shape2D::Circle(vec2(0.5, 0.5), 0.1);
circle->style.color = RGBA(0.8f, 0.1f, 0.1f, 1.f);
show << circle->at("circle_label");
```

### Builders

!!! note "```Shape2D::Line(a, b)``` / ```Bezier(a, control, b)``` / ```Circle(center, radius)``` / ```Rect(center, size)```"
!!! note "```Shape2D::Add(std::vector<vec2> points, bool closed)``` — arbitrary polyline"

Geometry is given in relative $[0,1]^2$ coordinates, then recentered around the anchor: shapes are placed, dragged and transitioned like any other screen primitive.

Every shape carries a ```ShapeStyle```: `color`, `fill_color`, `thickness` (pixels at 1080p, scaled with the window) and `filled`.

### Arrows

```Arrow2D``` is a connector: its endpoints are resolved **every frame**, so arrows follow drag edits and moving targets.

```c++
show << Arrow2D::Add(Arrow2D::Attach(formula),        // a screen primitive
                     Arrow2D::AttachLabel("target")); // a persistent label
```

An endpoint is a fixed position, a label, or a screen primitive — in which case the arrow attaches at the boundary of its bounding box, keeping a small `margin`. Each endpoint also takes an `offset`, applied after attachment, to fine-tune where the arrow starts and lands.

| Field | Effect |
| --- | --- |
| `bend` | curvature: control-point offset, as a fraction of the endpoint distance |
| `head` | arrowhead size, relative units |
| `margin` | gap kept between an endpoint and its target |
| `from.offset` / `to.offset` | shift of the attach points |

### Englobing boxes

```Box2D``` is a rectangle englobing other screen primitives: the union of their bounding boxes (plus `padding`) is recomputed every frame, so the box follows drag edits and hot-reloaded content.

```c++
auto box = Box2D::Add(theorem, formula);
box->style.filled = true;   // filled with the background color by default,
                            // or box->setFillColor(...)
show << box;
```

Like any primitive, the box is drawn at its insertion rank in the slide: add it *before* its targets to frame them, *after* to cover them.

In a deck manifest, arrows and boxes are available as the `arrow:` and `box:` items (see [manifest format](../../deck/manifest)).
