---
title: Automatic transitions
---

Slope handles automatically fade in/fade out, and primitive displacement between slides.

To do so, there is a distinction between a Primitive, which is a unique object, and a Primitive placed in a slide.

The difference being that if a primitive is present in a slide at a given location, and in the next slide at another location, the transition will be generated between the two:

```c++
    auto text = Title("follow me");
    show << text->at(TOP);
    show << inNextFrame << text->at(BOTTOM); // text will slide from top to bot

```
In this example the title is duplicated by ```inNextFrame``` but when you reinsert it, the new location overrides the old one.


<video width="100%" autoplay loop muted>
  <source src="../../static/transition.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

