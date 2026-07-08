---
title: C++ objects
---

## Registering C++ objects

Anything the manifest cannot express — updaters, computed geometry, quantities — is defined in C++ and registered under a name, then placed by the manifest with `object: name`.

```c++
    auto spot = Mesh::Add("spot.obj");
    spot->setUpdater([](TimeObject t){ /* ... */ }); // configure animation
    deck.registerObject("wobbly_spot",spot);
```

`registerObject` accepts several forms:

!!! note "```registerObject(name, std::function<PrimitiveInSlide()>)``` — factory, primitive + state"
!!! note "```registerObject(name, std::function<PrimitivePtr()>)``` — factory, default state"
!!! note "```registerObject(name, PrimitivePtr)``` / ```registerObject(name, PrimitiveInSlide)``` — already-built"
!!! note "```registerObject(name, PrimitiveGroup)``` (or its factory) — several primitives placed together"

Factories are called lazily, the first time the manifest uses the name, and the result is cached: a hot reload re-places the same primitive instead of rebuilding it, so meshes, textures and compiled latex survive edits.

### With tunable parameters

Registered objects combine naturally with [tunable parameters](../../interactivity): declare the parameter next to the updater that reads it, and tune the animation live while editing the deck.

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

### Synchronizing with the deck : keyframes

An updater branching on `t.relative_frame_number` assumes a step structure that the manifest can freely reorder. Instead, mark the relevant frame in the manifest with a [keyframe](../manifest#keyframes) and test it by name — the branch follows the label wherever it moves:

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
