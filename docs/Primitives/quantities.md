---
title: Polyscope Quantities
---

The most appealing feature of polyscope is arguably being able to visualize all kind of fields (of scalars or vectors).

Of course, during the presentation, one would like to control independently the quantity being visualized and the primitive it belongs to.

One can do it simply in the following way:
```c++

auto mesh = Mesh::Add("bunny.obj");

Vec V = // some scalar field of size = nb vertex;

auto sf = mesh->pc->addVertexScalarQuantity("some field",V);

auto field = AddPolyscopeQuantity(sf);

// displays mesh first, then the scalar field
show << mesh << InNextFrame << field;

```


