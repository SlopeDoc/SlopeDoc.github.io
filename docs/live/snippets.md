---
title: Lua snippets
---

Suppose that you want to plot a scalar field, but what should it look like? $\sin(xyz)$? $\cos(x)\cos(y)\cos(z)$? I don't know! But if you have to recompile at each guess, that's where crafting slides takes long. So instead, use snippets!

Snippets are also usefull to define variables/functions that are accessible everywhere so you can easily synchronize polyscope, shaders and even latex placement.

You can write them all in one `snippets.lua` file (or in several):

```lua title="snippets.lua"
--- envelope                      -- a value : one variable, named after the section
return math.sin(t.from_begin)

--- motion                        -- a table : one variable per key, flat
local swing = 0.5 * math.sin(t.from_begin)
return { center = vec2(swing, 0), radius = 0.5 + 0.1 * swing }

--- displace                        -- a function : a callable snippet
return function(x, y, z)
  local a = math.sin(x * 6 + t.from_begin) * math.cos(y * 6)
  return x, y, z + 0.15 * a
end

```

Then:

=== "C++"

    ```c++ title="main.cpp"
    Snippet::load("snippets.lua");     // resolved against the project data path
    ```

=== "Deck manifest"
    ```yaml title="deck.yaml"
    snippets: snippets.lua        # or a list of files
    slides:
        - ...
    ```


The interest is that those expression are hot-reloaded while the slides are running, so if you have them in an updater, you can tweak any formula and see the result instantly! 

All the variables defined in this file are in a common namespace (shared with [tunable parameters](params.md)) accessible from anywhere in your slides.

In C++ objects:
```c++
static auto displace = Snippet::fn<vec(scalar,scalar,scalar)>("displace");

mesh->updater = [mesh, V0](TimeObject) {
    vecs V = V0;
    for (size_t i = 0; i < V.size(); i++)
        V[i] = displace(V0[i](0), V0[i](1), V0[i](2)) * Snippet::get("envelope").num();
    mesh->updateMesh(V);
};
```

In shaders or screen placement, see [tracking](../placement/tracking.md#manifest-format):

```yaml title="deck.yaml"
- shader: myshader.frag
  id: fx
  view: {half: 2}       # its world space, needed to place anything on a point of it
  uniforms:
    - center            # feeds "uniform vec2 center;"
- latex: x
  follow: fx.center     # center, read in the referential of fx
```

### Built-ins

As all primitives, snippets have acess to a global TimeObject `t` to be time-varying. Just remember that in lua attributes are accessed with dots `t.from_begin`, while methods with: `t:afterKeyframe("test")`.

You also have Lua's `math`, `string`, `table`.

You can access to all (GUI-)tunable [parameters](params.md) as global variables and even declare new ones with:

```lua title="snippets.lua"
--- envelope
local speed = param("wave/speed", 1.2, 0, 4)   -- declared here, slider in the Tuner
return math.sin(t.from_begin * speed) * amplitude   -- declared elsewhere, read by its name
```

`param()` returns the live value, so a section reads it like any other number and follows the slider while the show runs. A parameter that already exists, declared in C++ or by another section, is read by its bare name ; declaring it again with the same call is harmless and returns it unchanged.

??? note "```param(name, default, min, max)```"
    - ```name``` the parameter's name, `"group/name"` grouping it in the Tuner panel
    - ```default``` its value until it is edited
    - ```min```, ```max``` slider bounds, optional ; equal (the default) means an unconstrained drag

    Declares a [tunable parameter](params.md) on first use and returns its live value. Only scalars are declared this way ; a `vec2`, `vec3` or color parameter declared in C++ is read by its bare name.

## Interaction with C++

!!! note "```Snippet::Value Snippet::get(const std::string& name)```"
    The value of a section, a table key, a parameter or a C++ derivation, evaluated on first read of the frame and memoized. An unknown or failing name gives a `Value` with `n == 0`, which converts to zero.

A `Value` carries its component count `n` and converts on assignment to `scalar`, `float`, `int`, `bool`, `vec2`, `vec` or `RGBA`. Passing one straight to a function is ambiguous, so name the one you meant:

```c++
integrate(Snippet::get("center").v2(), Snippet::get("radius").num());
```

### Doing the heavy lifting in C++

If some more intense computation must happen but that depends on a snippet, you can compute in C++ and send it back to the global namespace:

```c++
Snippet::derive("energy", [](const TimeObject&) { return totalEnergy(); });
```

??? note "```Snippet::derive(name, f)```"
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

??? note "```Snippet::derive(name, {deps...}, f)```"
    - ```deps``` the names it is computed from

    Recomputed only on a frame where one of `deps` differs from the frame before, and the previous result is returned otherwise. A lambda has to be wrapped in its `std::function` here, the dependency list making the return type ambiguous otherwise.

The same idea to gate an expensive rebuild:

```c++
if (Snippet::dirty({"center", "radius"}))
    rebuild();                       // skipped while they sit still
```

??? note "```bool Snippet::dirty(name | {names...}, const char* tag = nullptr)```"
    - ```names``` the values to watch
    - ```tag``` distinguishes two guards written on the same line

    True on the first call, then whenever one of the values has moved since *this call site* last asked. Keyed by call site, so two consumers of one variable never clear each other's flag.

??? note "```long Snippet::changed(const std::string& name)```"
    A counter bumped whenever the value differs from the previous frame's, to track by hand when one consumer watches many names.

## Snippet functions in shaders

A callable is also the way to hand a shader something a uniform cannot hold. A Lua closure cannot cross to the GPU, but its values can: sample it in C++ and upload the samples as a texture.

```c++
static auto profile = Snippet::fn<scalar(scalar)>("profile");
for (int k = 0; k < N; k++)
    grid[k] = float(profile(X0 + (X1 - X0) * (k + 0.5) / N));
fx->setTexture("profile", grid, N, 1, 1);
```
