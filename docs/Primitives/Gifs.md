---
title: Gifs
---

As screen primitives are rendered with ImGui, no video support is possible but one can load gifs instead:

```c++

show << Gif::Add("puppy_dance.gif");
```

??? note "```c++ Gif::Add(std::string path, int fps,float scale,bool loop); ```"
    - ```std::string path``` if relative then look in [data path](../../options).
    - ```int fps``` speed at which the gif is played (default: 10 fps)
    - ```float scale``` gif scale
    - ```bool loop``` does the gif repeat (default: true)


!!! warning "Warning"
    Gifs are simply decomposed in images (in a cache) and then rendered sequentially, hence it easily takes a lot of space.
