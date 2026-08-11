---
title: Video and Webcam
---

Want to play a demo? Run a video! Unlike Gifs, videos are streamed using ```ffmpeg``` to avoid excessive memory usage.

=== "C++"

    ```c++ title="main.cpp"
    #include "slope.h"
    using namespace slope;

    Slideshow show;

    int main(int argc, char** argv) {
        show.init("video_demo", argc, argv);
        show << Video::Add("clip.mp4")->at(CENTER);
        show.run();
        return 0;
    }
    ```

=== "Deck manifest"

    ```yaml title="deck.yaml"
    slides:
      - frame:
          - video: clip.mp4
            at: screen
    ```

### Builder

!!! note "```c++ Video::Add(std::string file, int decode_width = 0, bool loop = true, bool autoplay = true);```"
    - ```std::string file``` if relative then look in [data path](../../options).
    - ```int decode_width``` decode at this width, `0` meaning the window width.
    - ```bool loop``` restart at the end (default: true)
    - ```bool autoplay``` start playing as soon as the slide is reached
      (default: true). With `false` the first frame is held until clicked.


## Playing, pausing, speed

Click the clip to play or pause it. 

```c++
v->play();
v->pause();
v->togglePlay();
bool running = v->isPlaying();
```

Speed is a callable read every frame, so a [tunable parameter](../../interactivity)
can drive it live while you talk:

```c++
auto speed = Params::Add("video/speed", 1., 0., 3.);
v->speed = [speed] { return (scalar)speed; };
```

The smaller the video is, the cheaper it is to display. Please use the right
`decode_width` if you plan on playing it in a smaller size.
```c++
auto small = Video::Add("clip.mp4", 640);
```

Left at `0` it decodes at the window width. Note that this is the decode size,
not the display size: how big the clip appears on the slide is a matter of
[placement](../../placement/absolute) and `StateInSlide` like any other screen
primitive.

## Webcam

Whether you want to record your slides with your head moving around or do a live demo of an image effect
you can feed a video stream like your webcam:

=== "C++"

    ```c++
    show << Webcam::Add()->at(CENTER);
    ```

=== "Deck manifest"

    ```yaml title="deck.yaml"
    - webcam: /dev/video0
      at: cam
      width: 1280
      height: 720
      fps: 30
    ```

### Builder

!!! note "```c++ Webcam::Add(std::string device = \"/dev/video0\", int w = 1280, int h = 720, int fps = 30, std::string input_format = \"mjpeg\");```"
    - ```std::string device``` the v4l2 device node.
    - ```int w, int h, int fps``` the mode to open the device in.
    - ```std::string input_format``` `mjpeg` or `yuyv422`, most commonly.

## Snapshots

A frame can be pulled out of either primitive, which pairs with
[`Image::updateImage`](../images#changing-an-image-while-the-talk-runs) to drop
a still into a slide that is already running:

```c++
auto cam   = Webcam::Add();
auto still = Image::Blank(cam->decodedWidth(), cam->decodedHeight());

show << cam->at("cam")
     << still->at("still")
     << ImGuiWidgets::Add([cam, still]() {
            if (ImGui::Button("snapshot") && cam->saveFrame("/tmp/shot.png"))
                still->updateImage("/tmp/shot.png");
        }, "camera");
```

The button belongs in an [ImGui widget](../../interactivity), not in the
camera's `updater`. The widget opens and closes its own window around the
callback, and it is a primitive like any other, so the button is only on screen
while the slide is.

The `Image` has to be on the slide from the start, transparent, rather than
added when the button is pressed: the slideshow is already running by then, so
a snapshot refills a texture instead of inserting a primitive.

!!! note "```c++ std::vector<unsigned char> framePixels() const;```"
    The frame currently in the texture, RGBA, first row at the top.

!!! note "```c++ bool saveFrame(const std::string& file) const;```"
    Writes that frame to a png.

## Manifest format

```yaml
- video: clip.mp4       # streamed from disk, one ffmpeg pipe
  at: vid
  scale: 0.5            # default size (default: 1)
  decode_width: 960     # decode at this width (default: the window width)
  loop: false           # stop at the last frame instead of restarting
  autoplay: false       # hold the first frame until clicked
  speed: 2              # playback speed
  stats: true           # overlay the decode counters
```

```yaml
- webcam: /dev/video0   # a live camera
  at: cam
  scale: 0.5            # default size (default: 1)
  width: 1280           # the mode to open the device in, it is
  height: 720           # told and not probed
  fps: 30
  input_format: mjpeg   # the device's pixel format
  stats: true           # overlay the decode counters
```

Changing `scale`, `speed` or `stats` reloads without restarting the decoder. Changing
anything that shapes the decode, `decode_width` or a camera's mode, restarts
it, which is the honest cost of that change.
