---
title: Persistant
---

Eyeballing positions on the screen can be tedious, hence, you can instead assign a label to a primitive (possibly a different one per slide).

Labeled pritmives can then be selected, with ```Ctrl+Left Click```, and be moved with the mouse and scaled with the mouse roll.
A selected primitive can be centered horizontally by pressing ```H``` and vertically by pressing ```V```.

```c++
    show << slope_logo->at("label1");
    show << inNextFrame << slope_logo->at("label2"); // will move from label1 pos to label2 pos
```

!!! warning "Warning"
    Labels must be unique, if you set the same label to another primitive, they will share the same position (can be usefull to replace a primitive by another one).


<video src="../../static/persistant.mp4" muted autoplay loop controls width="100%" >
</video>


