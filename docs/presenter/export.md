---
title: Exporting to PDF
---

Slope can render your whole presentation to a PDF, one page per slide, without touching a screenshot key. Launch with ``--export`` instead of running the live show:

```
./project_exe --project_path /home/.../slope_project --export
```

This runs headless and writes ``<project_path>/<project name>.pdf`` in one pass. The project name is whatever you passed to ``show.init(...)`` (see the [tutorial](../tutorial)).

### What part of the slides are captured

- every primitive's clock is set to 10 seconds, to capture animation at a "rest pose", complex animations/GIFs cannot be properly captured (yet)
- the slide's camera is applied directly, skipping any [``flyTo`` flight](../Primitives/camera)
- a screenshot (including the ImGui-drawn UI, etc...) is taken for each slide, then all of them are concatenated into the PDF with ImageMagick's ``convert``

