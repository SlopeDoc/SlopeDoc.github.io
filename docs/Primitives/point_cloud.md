---
title: Point Clouds
---

What would we do without point clouds? You can load one as simple as:

### Builders

??? note "```c++ PointCloud::Add(const vecs& X,scalar radius = -1); ```"
    - ```const vecs& X``` ```std::vector<Eigen::Vector3d>```
    - ```float radius``` point cloud radius (not relative), if not set then polyscope default radius is used. It can also be the name of a [parameter](../../live/params) or a [snippet](../../live/snippets) variable, to tune it live.

??? note "```c++ PointCloud::Add(const std::string& file,scalar radius = -1); ```"
    - ```const std::string& file``` a ```.ply``` or ```.obj``` file, only its vertices are read

### Single Point

A single point, with more features, can be added using

!!! note "```c++ Point::Add(const vec& x,scalar radius = -1); ```"
??? note "```c++ Point::Add(const DynamicParam& x,scalar radius = -1); ```"
    - ```DynamicParam = std::function<vec(TimeObject)>``` the point follows a time-dependent position (wrapper for its [updater](../Animation))
??? note "```VectorFieldQuantity Point->addVector(const vec& v)```"
    - attaches a vector to the point, see [polyscope quantities](../quantities)

## Deck format

```yaml
- cloud: scan.ply       # a .ply or .obj file, relative to the data path
  radius: scan_radius   # a number, or a name to tune it live
  normalize: true       # rescale the cloud to fit the scene
  color: [0.2, 0.4, 0.8]
```

It also takes the `transform:` of every [scene item](../polyscope_primitives#deck-format).
