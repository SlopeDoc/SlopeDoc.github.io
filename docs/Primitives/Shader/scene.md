---
title: Interacting with the 3D scene
---
<video src="../../../static/shader_polyscope.mp4" muted autoplay loop controls width="100%" >
</video>

Shaders are rendered on top of polyscope. But you can make the two work together!
For instance, if you are doing any form of raytracing, by using the [Shader STL](stdlib.md)'s "camera.glsl", you can generate rays that follow the polyscope camera! (If you want to do custom stuff, polyscope camera is passed as uniforms).


```glsl
#include <camera.glsl>
void main() {
    vec3 ro, rd;
    polyscopeRay(ro, rd);
    // trace against ro/rd here
}
```

## Using polyscope depth buffer

To make polyscope objects coherent with a shader, you can use its depth buffer. Reach for `visibleOverScene` (or any of the other `scene*` functions in `camera.glsl`) and the buffer is passed on automatically:

## Minimal example

=== "C++"

    ```c++ title="main.cpp"
    #include "slope.h"
    using namespace slope;

    Slideshow show;

    int main(int argc, char** argv) {
        show.init("scene_demo", argc, argv);
        show << Mesh::Add("spot.obj");
        show << Shader::FromFile("occluded.frag")->at(CENTER);
        show.run();
        return 0;
    }
    ```

=== "Deck manifest"

    ```yaml title="deck.yaml"
    slides:
      - frame:
          - mesh: spot.obj
          - shader: occluded.frag
            at: screen
    ```

```glsl title="occluded.frag"
#include <camera.glsl>
#include <sdf.glsl>
#include <raymarch.glsl>

float sceneSDF(vec3 p) {
    vec3 q = p - vec3(0.9, 0.3, 0.0);
    float a = sdSphere(q, 0.22);
    vec3 orbit = vec3(0.22 * sin(iTime), 0.22 * cos(iTime), 0.0);
    float b = sdSphere(q - orbit, 0.13);
    return opSmoothUnion(a, b, 0.15);
}

void main() {
    vec3 ro, rd; polyscopeRay(ro, rd);
    vec3 pos;
    if (marchScene(ro, rd, pos) && visibleOverScene(pos)) {
        vec3 n = sceneNormal(pos);
        fragColor = vec4(shadeDefault(pos, n, rd, vec3(0.85, 0.25, 0.25), vec3(1.0)), 1.0);
    } else {
        discard;   // let the mesh show through instead
    }
}
```


??? note "When you need to activate the depth buffer"
    Currently, the scanner that checks if you need the depth buffer only reads the shader's own text, not what it pulls in through `#include`. A helper header of your own that wraps `visibleOverScene` internally won't be picked up, the shader that includes it has to call `shader->useSceneDepth()` from C++ instead, once.
