---
title: Point Clouds
---

What would we do without point clouds? You can load one as simple as:

### Builders

??? note "```c++ PointCloud::Add(const vecs& X,scalar radius = -1); ```"
    - ```const vecs& X``` ```std::vector<Eigen::Vector3d>```
    - ```float radius``` point cloud radius (not relative), if not set then polyscope default radius is used

### Single Point

A single point, with more features, can be added using

!!! note "```c++ Point::Add(const vec& x,scalar radius = -1); ```"
??? note "```c++ Point::Add(const DynamicParam& x,scalar radius = -1); ```"
    - ```DynamicParam = std::function<vec(TimeObject)>``` the point follows a time dependent (wrapper for its [updater](../../Animation))
??? note "```VectorFieldQuantity Point->addVector(const vec& v)```"
    - attachs a vector to the point, see [polyscope quantites](../quantities)
