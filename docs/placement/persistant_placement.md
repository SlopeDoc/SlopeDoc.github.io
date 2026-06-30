---
title: Persistent
---

Eyeballing positions on the screen can be tedious, hence, you can instead assign a label to a primitive (possibly a different one per slide).

Labeled primitives can be selected with ```Ctrl+Left Click```, then moved with the mouse and scaled with the mouse wheel. While you drag, light-blue guides appear and snap the primitive's edges and center to the other primitives of the slide, so you can align elements precisely. A selected primitive can also be centered horizontally by pressing ```H``` and vertically by pressing ```V```.

Dragged positions are kept only for the current session until you save them: press ```Ctrl+S``` to write them to disk so they are restored on the next run. If you try to quit (```Esc```) with unsaved placements, Slope asks for confirmation first.

```c++
    show << slope_logo->at("label1");
    show << inNextFrame << slope_logo->at("label2"); // will move from label1 pos to label2 pos
```

!!! warning "Warning"
    Labels must be unique, if you set the same label to another primitive, they will share the same position (can be usefull to replace a primitive by another one).


<video src="../../static/persistant.mp4" muted autoplay loop controls width="100%" >
</video>


