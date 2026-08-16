---
title: World to screen tracking
---

A screen primitive can be placed on a moving point rather than at a fixed position. The point is re-read every frame, so a label stays on the object, or on the pixel, it names.

The point lives in one of three spaces: the 3D scene, the world space of a [shader](../../Primitives/Shader/basics#view-the-shaders-world-space), or the screen.

## A point of the 3D scene

You can force a 2D object, for instance a label, to follow a 3D object of the scene using the ```screenprimitiveptr->track``` method.

!!! note "```track(const std::function<vec()>& placer,vec2 offset)```"
    - ```const std::function<vec()>& placer``` should return the 3D position to follow, the lambda is intended to capture the element to follow, see Example.
    - ```vec2 offset``` displacement on the screen from the projected 3D position, expressed in relative coordinates (i.e. ```vec2(0.1,0.2)``` means an offset of 10% of the screen width and 20% of the screen height)

### Example

```c++
    auto particle = Point::Add([] (TimeObject t) -> vec {
        float angle = t.inner_time;
        return vec(cos(angle), sin(angle), 0);
    });

    show << particle;

    show << Formula::Add("x")->track([particle] () {return particle->getCurrentPos();}, vec2(0.03,0.03));
```
<video src="../../static/tracking.mp4" muted autoplay loop width="100%" >
</video>

A fixed point in the 3D scene can also be followed:
!!! note "```at(const vec& pos,vec2 offset)```"

## Following a point of a shader

A shader given a `view:` draws a known region of the plane, so its world points can be followed. `tracker` turns one into a placer:

```c++
fx->setView(vec2(0, 0), 3.2);                   // 3.2 world units above the middle
show << eq->at(fx->tracker(vec2(1, 0)));        // sits on the point z = 1
show << lbl->at(fx->tracker([]{ return Snippet::get("center").v2(); }, vec2(0.025, -0.03)));
```

!!! note "```tracker(const vec2& world, vec2 offset)```, also taking a ```std::function<vec2()>```"

The point is read through the view and rect the shader was last drawn with, so the label agrees with the pixels under it whatever its placement and `resolution:`. The view itself can move (`bindView`), and the label follows.

## Manifest format

`follow:` is the manifest form of both: an item placed on a moving value rather than at a position.

```yaml
- latex: here
  follow: query_point     # a 3D point of the scene, projected every frame
- formula: p
  follow: fx.center       # "center", read in the world space of the shader "fx"
  offset: [0.025, -0.03]  # shifted from that point, in screen units
```

The name is a [snippet variable](../../live/snippets), a [tunable parameter](../../live/params), or a placer registered with `registerPlacer`. Its width says which space it is in:

| Components | Meaning |
| --- | --- |
| 3 | a point of the 3D scene, projected to the screen, like `track` above |
| 2 | a screen position, `0..1` with `y` up |
| 2, with an `<item>.` prefix | a point of the world space of that shader |

Nothing is inferred: a prefix naming something that is not a shader, a shader with no `view:`, a 3D value asked for in a shader's space, or a name resolving to nothing, each says so. A prefix is only read as one when it really names an item, so a parameter with a dot in its name is read whole.

!!! warning "`follow:` takes no `at:`"
    The item rides a moving point, so it has no position of its own to place. Use `offset:` to shift it from that point.
