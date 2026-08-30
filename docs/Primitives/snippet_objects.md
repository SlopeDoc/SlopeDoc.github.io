---
title: Snippet objects
---

If you want to create parameterized pritmives from functions, you can and should do it by using snippets to tune their shapes as you'd like them to be, directly in a deck and with lua snippets.

## Surfaces

Surfaces can be created from, possibly time-dependant, parameterizations, taking a `vec2` and returning a `vec3`:

```lua title="snippets.lua"
--- wave
return function(uv)
  return vec3(uv.x, uv.y, 0.2 * math.sin(6 * uv.x + t.from_begin))
end
```

```yaml title="deck.yaml"
- surface: wave
  u: [0, 6.2832]        # the parameter domain, [0,1] by default
  v: [0, 6.2832]
  resolution: [96, 48]  # its grid, a single number for a square one
  closed: [true, true]  # welds the seam of a periodic domain
  at: wave_transform    # a persistent transform, as for a mesh
```

Editing the domain or the resolution reconfigures the object in place, so you can tune the grid while the show runs.

??? note "```SnippetSurface::Add(const std::string& fn,int resolution = 64)```, also taking a ```Spec```"
    The ```Spec``` carries the same fields as the manifest: ```fn```, ```u```, ```v```, ```res_u```, ```res_v```, ```closed_u```, ```closed_v``` and ```smooth```.

## Curves

A curve is the same over a segment, from one number to a `vec3`:

```lua title="snippets.lua"
--- helix
return function(s)
  return vec3(math.cos(s + t.from_begin), math.sin(s + t.from_begin), 0.15 * s)
end
```

```yaml title="deck.yaml"
- curve: helix
  u: [0, 12.566]
  resolution: 400       # nodes along the segment, 200 by default
  closed: false         # true joins the last node back to the first
  radius: 0.01          # left to polyscope when omitted
```

!!! note "```SnippetCurve::Add(const std::string& fn,int resolution = 200)```, also taking a ```Spec```"

## Points

A single point rides a snippet variable, or a given world coordinate:

```yaml
- point: apex           # follows the variable "apex"
- point: [0, 0, 1]
  radius: 0.02
```

<!-- <video src="../../static/snippet_objects.mp4" muted autoplay loop controls width="100%" >
</video> -->
