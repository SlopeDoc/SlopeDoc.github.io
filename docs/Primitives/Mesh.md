---
title: Mesh
---

What would we do without meshes? You can load one either from a file or a handmade one:


### Builders

??? note "```c++ Mesh::Add(std::string path, float scale,bool smooth = true); ```"
    - ```std::string path``` if relative then look in [data path](../../options).
    - ```float scale``` scale 
    - ```bool smooth``` polyscope shading mode (if false then visible edges)


??? note "```c++ Mesh::Add(const vecs& V,const faces& F, bool smooth = true); ```"
    - ```const vecs& V``` vecs = ```std::vector<Eigen::Vector3d>```.
    - ```const faces& F``` faces = ```std::vector<std::vector<size_t>```.
    - ```bool smooth``` polyscope shading mode (if false then visible edges)

## Scalar fields

While you could display a scalar field by using the common approach of [Quantities](../quantities), 
slope offers a custom wrapper for scalar fields for a proper continuous intro/outro display.

??? note "```c++ MeshScalarField::Add(const Mesh::MeshPtr& mesh, const std::string& name, const Vec& values, const std::string& colormap = 'viridis'); ```"
    - ```const Mesh::MeshPtr& mesh``` the mesh carrying the field.
    - ```const std::string& name``` the quantity name, as polyscope shows it.
    - ```const Vec& values``` one value per vertex (```scalars``` also accepted).
    - ```const std::string& colormap``` any polyscope colormap.

    ```void setBaseline(scalar v)``` the value every vertex starts from,
      the field's minimum by default.


    ```scalar color_split``` fraction of the intro spent fading the mesh
      colour to ```colormap(baseline)``` before the field grows, so the surface
      colour does not pop. ```0``` disables that stage.



## Manifest format

```yaml
- mesh: bunny.obj       # the obj file, relative to the data path
  at: bunny_transform   # a persistent transform label, not a screen position
  smooth: false         # polyscope shading mode, false shows the edges
  normalize: true       # rescale the mesh to fit the scene
```
