---
title: Timed pauses
---

If, despite your best efforts, you tend to speak too fast during presentations, slope has the solution for you: forced breaks!

Instead of directly going to the next slide when you press ``right arrow``, if you added a ``Pause(t)`` to the current slide, then it will take ``t`` seconds before going to the next slide!

```c++
    show << Mesh::Add("bunny.obj");
    show << Pause::Add(2.0); // will hold this slide for 2 seconds before moving forward
    show << newFrame << Title("Done!")->at(TOP);
```

