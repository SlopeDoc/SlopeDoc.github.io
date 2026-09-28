---
title: Basics
---
- [Point cloud](../point_cloud)
- [Mesh](../Mesh)
- Curve3D
- [Camera view](../camera)
- [Polyscope quantities](../quantities)

Polyscope primitives live in a common 3D referential.

You can edit all the properties of the polyscope object this way:

``` c++

    auto M = Mesh::Add("bunny.obj");
    M->pc->setSurfaceColor(glm::vec3(1,0,0));
    show << M; //red bunny
```

### Color

!!! note "```setColor(const Color& c)```"
    - ```Color(r, g, b)```, or ```Color("name")``` to read a [parameter](../../live/params) or a [snippet](../../live/snippets) variable, so the color can be tuned or animated.

## Deck format

Every scene item (`mesh`, `cloud`, `curve`, `surface`, `point` and `object`) takes a `transform:`, and all but `object` take a `color:`:

```yaml
- mesh: bunny.obj
  color: "#d08040"          # [r, g, b], "#rrggbb", or a name
  transform:
    pos: [0, 0.5, 0]
    scale: 2                # a number, or [x, y, z]
    axis: [0, 1, 0]         # rotation axis, z by default
    angle: 45               # in degrees
```

Each field can also be the name of a parameter or a snippet variable, read every frame, so the object can be tuned or animated from the deck. With `at: <label>`, the transform is applied inside that label, which the gizmo still moves.

