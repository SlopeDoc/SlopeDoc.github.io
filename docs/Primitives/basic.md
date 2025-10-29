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

The key difference being that screen primitives can be placed on the screen using various 2D referential (see [Placement](../../placement/relative_placement)), while polyscope ones
can be displaced in the scene or viewed from different camera angles.


Most primitives can be instanciated using:

``` c++
    // PrimitiveType::Add( contructor );
    // like
    Mesh::Add("bunny.obj");

```
