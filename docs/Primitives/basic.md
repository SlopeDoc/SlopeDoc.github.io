---
title: Basics
---


Slope does a distinction between two types of Primitives, the ones that live only in the 2D screen and the ones that live in the Polyscope 3D engine.

## Screen Primitives

- Image
- Gif
- Latex

## Polyscope Primitives

- Point cloud
- Mesh
- Curve3D
- Camera view

The key difference being that screen primitives can be placed on the screen using various 2D referential, with the ```at``` method (see [Placement](../../placement/relative_placement)), while polyscope ones live in a common 3D referential (you can modify the model-to-scene transform by setting ```polyscopeprimitive->transform```).


Most primitives can be instanciated using:

``` c++
    // PrimitiveType::Add( contructor );
    // like
    Mesh::Add("bunny.obj");
```
