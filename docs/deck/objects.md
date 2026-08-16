---
title: C++ objects
---

## Registering C++ objects

Anything the manifest cannot express (computed geometry, quantities, a simulation step) is defined in C++ and registered under a name, then placed by the manifest with `object: name`.

Register an object for the computation, not for the choreography: a value that only needs tuning is a [parameter](../../live/params), and the shape of a motion can be a [snippet](../../live/snippets).

```c++
    auto spot = Mesh::Add("spot.obj");
    spot->setUpdater([](TimeObject t){ /* ... */ }); // configure animation
    deck.registerObject("wobbly_spot",spot);
```

`registerObject` accepts several forms:

!!! note "```registerObject(name, std::function<PrimitiveInSlide()>)```: factory, primitive + state"
!!! note "```registerObject(name, std::function<PrimitivePtr()>)```: factory, default state"
!!! note "```registerObject(name, PrimitivePtr)``` / ```registerObject(name, PrimitiveInSlide)```: already-built"
!!! note "```registerObject(name, PrimitiveGroup)``` (or its factory): several primitives placed together"

Factories are called lazily, the first time the manifest uses the name, and the result is cached: a hot reload re-places the same primitive instead of rebuilding it, so meshes, textures and compiled latex survive edits.

### Keeping the tunable part out of C++

Even a heavy updater reads *numbers*, which need not be compiled in. Declare a [parameter](../../live/params) next to the updater that reads it, and tune it live:

```c++
deck.registerObject("wobbly_spot", []() {
    auto amp = Params::Add("spot/amplitude", 0.2, 0., 0.5);
    auto spot = Mesh::Add("spot.obj");
    spot->setUpdater([=](TimeObject t){
        deform(spot, (scalar)amp, t.inner_time);
    });
    return spot;
});
```

When what you keep editing is the *shape* of the motion rather than a constant, read it from a [snippet](../../live/snippets) and the C++ side stops changing:

```c++
spot->setUpdater([=](TimeObject t){
    deform(spot, Snippet::get("amp"), Snippet::get("phase"));
});
```

The mesh, the deform loop and the upload stay compiled; the amplitude and the phase are a file you save.

### A registered shader keeps its manifest inputs

A shader registered from C++ for an updater, a multi-pass setup or a data texture does not lose the declarative layer with it: [`uniforms:`, `textures:` and `view:`](../../Primitives/Shader/basics#on-a-shader-registered-from-c) apply to an `object:` as to a `shader:` item.

```yaml
- object: field
  view: {half: 2}
  uniforms:
    - reveal          # a snippet variable, fed with no C++ in the path
```

### Synchronizing with the deck : keyframes

An updater branching on `t.relative_frame_number` assumes a step structure that the manifest can freely reorder. Instead, mark the relevant frame in the manifest with a [keyframe](../manifest#keyframes) and test it by name: the branch follows the label wherever it moves:

```yaml
- object: wobbly_spot
- step
- keyframe: noise_on
```

```c++
spot->setUpdater([=](TimeObject t){
    if (t.afterKeyframe("noise_on"))
        addNoise(spot, t.inner_time);
});
```

`afterKeyframe` is true from the marked frame on, `atKeyframe` exactly on it, `beforeKeyframe` strictly before. An unknown label warns once in the terminal and answers false.

A keyframe is also a *clock* and a *weight*, which lets an updater ease and blend rather than only switch: see [animation](../../Primitives/Animation#counting-from-a-keyframe).
