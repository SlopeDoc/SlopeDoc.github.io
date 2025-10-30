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

