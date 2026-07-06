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

!!! note "```ImGuiWidgets::Add(std::function<void()>& callback,std::string window_name)```"

<video width="100%" autoplay loop muted>
  <source src="../static/interactivity.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Tunable parameters

For animation constants (an amplitude, a speed, a color...), `Params` declares named, runtime-tunable, **persistent** parameters next to the code that uses them:

```c++
auto amp   = Params::Add("wobble/amplitude", 0.2, 0., 1.);  // slider in [0,1]
auto speed = Params::Add("wobble/speed", 1.);               // unconstrained drag

spot->setUpdater([=](TimeObject t) {
    deform(spot, (scalar)amp, (scalar)speed * t.inner_time);
});
```

!!! note "```Params::Add(name, default, min, max)``` — also ```AddInt```, ```AddBool```, ```AddColor```"

The handle reads the live value (a plain conversion, usable in hot loops). Pressing ``A`` opens the **Tuner** panel, showing the parameters read by the current slide's updaters (a checkbox reveals all of them), grouped by their `"group/name"` prefix. The polyscope camera is not affected while you tweak.

Edited values are saved with ``Ctrl+S`` to `views/params.json` — only ever-edited parameters are written, so untouched ones keep following their code defaults. The file is loaded back on startup, and hot-reloaded when edited by hand.

