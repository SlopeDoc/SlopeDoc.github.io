---
title: C++ objects
---

## Registering C++ objects

Anything the manifest cannot express — updaters, computed geometry, quantities — is defined in C++ and registered under a name, then placed by the manifest with `object: name`.

```c++
// a factory : called once, the primitive is cached across hot reloads
deck.registerObject("wobbly_spot", []() {
    auto spot = Mesh::Add("spot.obj");
    spot->setUpdater([](TimeObject t){ /* ... */ });
    return spot;
});
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

!!! warning "Steps are owned by the manifest"
    An updater branching on `t.relative_frame_number` assumes a step structure that the manifest can freely reorder — keep such assumptions in mind when editing the deck.
