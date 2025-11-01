---
title: World to screen tracking
---

You can force a 2D object, for instance a label, to follow a 3D object of the scene using the ```screenprimtiveptr->track``` method.

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
