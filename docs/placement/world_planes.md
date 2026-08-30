---
title: World planes
---

`at` puts a screen primitive somewhere on the screen. `onPlane` puts it in the 3D scene instead, flat on a plane, so it turns with the camera and stays on whatever it is labelling.

```cpp
show << Formula::Add("\\mathbf{n}")->onPlane("wall");
```

The name works like a [persistent label](../persistant_placement), except that it names a transform rather than a screen position: press ```T``` to place the plane with the gizmos.

### Explicit construction

You can also give the plane parameters yourself, as an origin, an in-plane direction and a normal:

!!! note "```onPlane(const vec& origin,const vec& u,const vec& normal,scalar alpha = 1)```"
    The item is as wide as ```u``` is long, and its height follows from its own aspect ratio.

```cpp
show << fig->onPlane(vec(0,0,0), vec(0.6,0,0), vec(0,0,1));
```

## Manifest format

`on:` is the manifest form of both.

```yaml
- image: chart.png
  on: wall              # a plane placed with the T gizmo
  two_sided: true       # also drawn from behind
- formula: \mathbf{n}
  on: {origin: p, u: e1, normal: nor}
```

In the second form each of the three is either three numbers, or the name of a [snippet variable](../../live/snippets) re-read every frame. 

!!! warning "`on:` takes no other placement"
    The item lives in the scene, so there is no screen position left to set: `at:`, `follow:` and `below:`/`above:`/`right_of:`/`left_of:` are refused next to it.

<!-- <video src="../../static/world_planes.mp4" muted autoplay loop controls width="100%" >
</video> -->
