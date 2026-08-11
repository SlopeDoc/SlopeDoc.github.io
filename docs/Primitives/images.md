---
title: Images and Gifs
---

The most basic screen primitives: a still picture, and a short animated one.

## Images

```c++
show << Image::Add("slope_logo.png");
```

### Builder

!!! note "```c++ Image::Add(std::string path, float scale);```"
    - ```std::string path``` if relative then look in [data path](../../options).
    - ```float scale``` image scale

### Changing an image while the talk runs

An image is usually a file read once, but its pixels can be replaced at any
time. 

You can also create a placeholder to be replaced with an image in a live demo:

```c++
// on the slide from the start, transparent until something fills it
auto still = Image::Blank(1280, 720);

show << still->at("still");
```

```c++
still->updateImage("/tmp/shot.png");        // from a file
still->updateImage(pixels.data(), w, h);    // from RGBA pixels, first row on top
```

!!! note "```c++ void updateImage(const unsigned char* rgba, int w, int h);```"
    Replaces the pixels. RGBA, first row at the top. A size change reallocates,
    so a source that switches resolution is fine, and a null pointer clears to
    transparent.


## Gifs

```c++
show << Gif::Add("puppy_dance.gif");
```

### Builder

??? note "```c++ Gif::Add(std::string path, int fps, float scale, bool loop); ```"
    - ```std::string path``` if relative then look in [data path](../../options).
    - ```int fps``` speed at which the gif is played (default: 10 fps)
    - ```float scale``` gif scale
    - ```bool loop``` does the gif repeat (default: true)

!!! warning "Warning"
    Gifs are simply decomposed in images (in a cache) and then rendered
    sequentially, hence it easily takes a lot of space. For anything longer than
    a few seconds, prefer [Video](../video), which streams instead of holding
    every frame.

See the [manifest format](../../deck/manifest) for the placement keys.

## Manifest format

```yaml
- image: figure.png     # the file, relative to the data path
  at: fig               # placement, defaults to a label from the filename
```
