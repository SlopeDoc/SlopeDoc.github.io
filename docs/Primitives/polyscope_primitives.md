---
title: Basics
---
- [Point cloud](../point_cloud)
- [Mesh](../Mesh)
- Curve3D
- [Camera view](../camera)

Polyscope primitives live in a common 3D referential.

You can edit all the properties of the polyscope object this way:

``` c++

    auto M = Mesh::Add("bunny.obj");
    M->pc->setSurfaceColor(glm::vec3(1,0,0));
    show << M; //red bunny
```
The object to scene transform can be set with:
``` c++ 
    
    auto M = Mesh::Add("bunny.obj");
    M->localTransform = Transform::ScalePositionRotate(...);

```
