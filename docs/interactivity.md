---
title: Interactivity & Widgets
---

Since Slope works on top of polyscope, you keep the control over the camera with usual mouse control.

To make interactive presentations, we can use ImGui widgets as a primitive:
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

