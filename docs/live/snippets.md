---
title: Lua snippets
---

One `.lua` file, split into sections by a `--- name` line (a legal Lua comment, so the file still highlights as Lua). What a section *returns* decides what it becomes:

```lua title="snippets.lua"
--- envelope                      -- a value : one variable, named after the section
return math.sin(t.from_begin * speed)

--- motion                        -- a table : one variable per key, flat
local swing = 0.5 * math.sin(t.from_begin)
return { center = vec2(swing, 0), radius = 0.5 + 0.1 * swing }

--- wobble                        -- a function : a callable snippet
return function(p, i)
  return p + vec3(0, 0, envelope * math.exp(-20 * p:norm()^2))
end
```

Sections see `t`, the built-ins below, and every other name in the namespace; reading another section evaluates it, so their order does not matter. Load the file from C++:

```c++
Snippet::load("snippets.lua");     // resolved against the project data path
```

or, in a deck, from the top of the manifest, next to `latex:` and `commands:`:

```yaml title="deck.yaml"
snippets: snippets.lua        # or a list of files
slides:
  - ...
```

!!! note "One namespace, shared with the parameters"
    Snippet variables and [tunable parameters](params.md) share one namespace. `param("motion/speed", 1.2, 0, 4)` declares one from Lua with its slider bounds and returns its live value; an existing parameter is read by its bare name.

### When a section runs

A section runs at most once a frame, on first read, and not at all on a slide that never asks for it. It does run on every frame it *is* read on, so heavy work belongs in a `derive()` with dependencies rather than in a section.

### What `t` gives you

`t` is the frame's [TimeObject](../Primitives/Animation.md), field for field:

| | |
| --- | --- |
| `t.from_begin` | seconds since the show started, the free running clock an animation usually wants |
| `t.from_action` | seconds since the last slide change |
| `t.delta_time`, `t.absolute_frame_number`, `t.transition_parameter` | as in C++ |
| `t:afterKeyframe(n)`, `t:beforeKeyframe(n)`, `t:atKeyframe(n)` | the keyframe tests |
| `t:secondsSince(n)`, `t:slidesSince(n)` | distance from a keyframe, in seconds and in slides |
| `t:during(a)`, `t:during(a, b)`, with a trailing `true` for sequential | the [blend weights](../Primitives/Animation.md#blending-states-instead-of-easing-them) |

A snippet has no moment of appearing, so there is no `inner_time` and no `relative_frame_number` (the per-primitive shader uniforms of those names do exist). `t:during("a")` and `t.during("a")` both work.

### Built-ins

Besides `t`, a section sees Lua's `math`, `string`, `table` and the usual small functions, plus:

!!! note "```param(name, default, min, max)```"
    - ```name``` the parameter's name, `"group/name"` grouping it in the Tuner panel
    - ```default``` its value until it is edited
    - ```min```, ```max``` slider bounds, optional ; equal (the default) means an unconstrained drag

    Declares a [tunable parameter](params.md) on first use and returns its live value. Only scalars are declared this way ; a `vec2`, `vec3` or color parameter declared in C++ is read by its bare name.

!!! note "```vec2(x, y)```, ```vec3(x, y, z)```, ```complex(re, im)```"
    Missing arguments are 0. Fields `.x .y .z`, and `.re .im` on a complex.

Methods, called with a colon:

| | |
| --- | --- |
| `a:norm()` | length, and `a:abs()` on a complex |
| `a:dot(b)` | scalar product |
| `a:cross(b)` | `vec3` only |

A value crossing into or out of Lua carries 1 to 4 components. One is a number, two or three a `vec2`/`vec3` (or a complex, if that is what made it), and four a plain array of four numbers, which is how a color arrives. A section may equally return an array of 1 to 4 numbers instead of a userdata.

Anything heavier than this stays in C++ and is only *gated* from Lua.

## Reading from C++

```c++
#include "content/Snippet.h"

vec2   c   = Snippet::get("center");    // converts to scalar, int, vec2, vec, RGBA
scalar env = Snippet::get("envelope");
```

!!! note "```Snippet::load(const path& file)```"
    Adds a snippet file, resolved against the project data path. Idempotent, and unnecessary in a deck, where `snippets:` does it.

!!! note "```Snippet::Value Snippet::get(const std::string& name)```"
    The value of a section, a table key, a parameter or a C++ derivation, evaluated on first read of the frame and memoized. An unknown or failing name gives a `Value` with `n == 0`, which converts to zero.

A `Value` carries its component count `n` and converts on assignment to `scalar`, `float`, `int`, `bool`, `vec2`, `vec` or `RGBA`. Passing one straight to a function is ambiguous, so name the one you meant:

```c++
integrate(Snippet::get("center").v2(), Snippet::get("radius").num());
```

!!! note "```v.num()```, ```v.v2()```, ```v.v3()```, ```v.rgba()```, ```v.valid()```"
    The same conversions, spelled out. `valid()` is `n > 0`.

!!! note "```Snippet::ok()```, ```Snippet::lastError()```, ```Snippet::names()```"
    Whether every section evaluated this frame, the last message, and every published name.

### Publishing back, and skipping work

C++ publishes **into** the namespace too, lazily, so something Lua has no business computing still reaches the deck and the shaders:

```c++
Snippet::derive("energy", [](const TimeObject&) { return totalEnergy(); });
```

!!! note "```Snippet::derive(name, f)```"
    - ```name``` the name it is published under, read like any other
    - ```f``` a callable of `const TimeObject&` returning `scalar`, `vec2`, `vec` or a `Value`

    Evaluated lazily, on the first read of each frame, and not at all on a frame that never reads it.

With a dependency list it is recomputed only when one of those values moves, and the result is cached:

```c++
Snippet::derive("energy", {"center", "radius"}, std::function<scalar(const TimeObject&)>(
    [](const TimeObject&) {
        return integrate(Snippet::get("center").v2(), Snippet::get("radius").num());
    }));
```

!!! note "```Snippet::derive(name, {deps...}, f)```"
    - ```deps``` the names it is computed from

    Recomputed only on a frame where one of `deps` differs from the frame before, and the previous result is returned otherwise. A lambda has to be wrapped in its `std::function` here, the dependency list making the return type ambiguous otherwise.

The same idea from the consuming side, to gate an expensive rebuild:

```c++
if (Snippet::dirty({"center", "radius"}))
    rebuild();                       // skipped while they sit still
```

!!! note "```bool Snippet::dirty(name | {names...}, const char* tag = nullptr)```"
    - ```names``` the values to watch
    - ```tag``` distinguishes two guards written on the same line

    True on the first call, then whenever one of the values has moved since *this call site* last asked. Keyed by call site, so two consumers of one variable never clear each other's flag.

!!! note "```long Snippet::changed(const std::string& name)```"
    A counter bumped whenever the value differs from the previous frame's, to track by hand when one consumer watches many names.

## Callable sections

A section returning a function is not a value but a **callable**: it is not evaluated per frame, it is called, as often as you like, with arguments. This is where a snippet stops being a schedule and becomes the body of a loop, a curve, a deformation, a colour map.

```lua title="snippets.lua"
--- displace
-- one vertex in, one vertex out
return function(x, y, z)
  local a = math.sin(x * 6 + t.from_begin) * math.cos(y * 6)
  return x, y, z + 0.15 * a
end
```

```c++
// resolved once, outside the loop : the name lookup costs more than the call
static auto displace = Snippet::fn<vec(scalar,scalar,scalar)>("displace");

mesh->updater = [mesh, V0](TimeObject) {
    vecs V = V0;
    for (size_t i = 0; i < V.size(); i++)
        V[i] = displace(V0[i](0), V0[i](1), V0[i](2));
    mesh->updateMesh(V);
};
```

The mesh, the loop and the upload stay in C++; the shape of the bump is a file you save. Every constant in it, the `6`, the `0.15`, the phase, can be a `param()` and get a slider.

!!! note "```Snippet::fn<R(A...)>(const std::string& name, R fallback = R())```"
    - ```name``` the callable section
    - ```fallback``` returned whenever the section is missing, not callable, or fails
    - ```R```, ```A...``` any of `scalar`, `float`, `int`, `vec2`, `vec`

    `valid()` says whether the name resolved. The handle survives a hot reload, its chunk re-resolved underneath, so it can be `static` in an updater.

A callable is also the way to hand a shader something a uniform cannot hold. A Lua closure cannot cross to the GPU, but its values can: sample it in C++ and upload the samples as a texture.

```c++
static auto profile = Snippet::fn<scalar(scalar)>("profile");   // 1024 calls, about 0.15 ms
for (int k = 0; k < N; k++)
    grid[k] = float(profile(X0 + (X1 - X0) * (k + 0.5) / N));
fx->setTexture("profile", grid, N, 1, 1);
```
