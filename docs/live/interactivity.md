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
  <source src="../../static/interactivity.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Widgets, or parameters ?

A widget is for values the audience should see you change, and costs a heap-allocated value and a callback.

A value you are only tuning while preparing is a [tunable parameter](params.md) instead: one line, a slider in the Tuner panel, saved to disk. Anything with more structure than a number is a [Lua snippet](snippets.md).
