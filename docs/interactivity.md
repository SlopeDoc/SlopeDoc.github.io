---
title: Interactivity & Widgets
---

Since Slope works on top of polyscope, you keep the control over the camera with usual mouse control.

To make interactive presentations, you can use ImGui widgets as a primitive:
```c++
    float* f = new float(1); // make sure to allocate on heap

    show << Point::Add([f](TimeObject t) {
        scalar th = (*f)*t.inner_time;
        return vec(cos(th),sin(th),0);
    });

    show << ImGuiWidgets::Add([f]() {
        ImGui::SliderFloat("speed",f,0,10);
    },"window name");
```

!!! note "```ImGuiWidgets::Add(const std::function<void()>& callback,std::string window_name)```"

<video width="100%" autoplay loop muted>
  <source src="../static/interactivity.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Tunable parameters

For scalar-like parameters that need tuning for animation, you can add a `Params` object: runtime-tunable, **persistent** parameters declared next to the code that uses them:

```c++
auto amp   = Params::Add("amplitude", 0.2, 0., 1.);  // slider in [0,1]
auto speed = Params::Add("speed", 1.);               // unconstrained drag

spot->setUpdater([=](TimeObject t) {
    deform(spot, (scalar)amp, (scalar)speed * t.inner_time);
});
```

!!! note "```Params::Add(name, default, min, max)```, also ```AddInt```, ```AddBool```, ```AddColor```, ```AddVec2```, ```AddVec```, ```AddDir```"

The handle reads the live value (a plain conversion, usable in hot loops). Pressing ``A`` opens the **Tuner** panel, showing the parameters read by the current slide's updaters (a checkbox reveals all of them), grouped by their `"group/name"` prefix. The polyscope camera is not affected while you tweak.

Edited values are saved with ``Ctrl+S`` to `views/params.json`. Only ever-edited parameters are written, so untouched ones keep following their code defaults. The file is loaded back on startup, and hot-reloaded when edited by hand.

### Handles

A position is easier to aim than to type, so the geometric parameters carry a widget on top of their sliders:

| Type | Button | Widget |
| --- | --- | --- |
| `vec3` | `3D` | a translation gizmo in the scene, the same one the `T` editor uses for transforms |
| `dir` (`AddDir`) | | a ball oriented like the camera: the mouse aims the unit vector, right click flips the hemisphere |
| `vec2` | `2D` | a crosshair dragged on the screen |

`all` and `none`, next to the panel's checkbox, switch every handle of the listed parameters on or off at once. While a handle is live the slide stops taking mouse input, so dragging never spins the camera by accident, and closing the panel puts everything back.

A `vec2` parameter is in **screen coordinates**: `0..1` across the window, `y` up. That is `gl_FragCoord`'s convention, the opposite of the screen anchors', and it is what lets a shader put an object exactly under its handle:

```glsl
#include <camera.glsl>
uniform vec2 center;

void main() {
    float d = length((screenPoint() - center) * iWindowSize);   // window pixels
    ...
}
```

`screenPoint()` reports where this fragment falls on the window, so the agreement holds wherever the shader is placed and whatever its `resolution:` is. It is the 2D counterpart of `polyscopeRay` for [3D scenes](Primitives/Shader/scene.md).

