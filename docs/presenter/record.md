---
title: Recording a video
---

If you want to export the animations in a talk as a video, or want it to play in a loop
at a poster session, `--record` renders the whole deck to an mp4, transitions
included.

```
./project_exe --project_path /home/.../slope_project --record
```

It runs without any interaction and writes `<project_path>/<project name>.mp4`. Each slide
change is played frame by frame, then the settled slide is held with its
animations still running.

| Flag | Effect | Default |
| --- | --- | --- |
| `--record` | render the deck to an mp4 and quit | |
| `--fps <n>` | frame rate of the video | 30 |
| `--record_dwell <s>` | seconds each settled slide is held | 2 |

The frames go to a temporary folder and are encoded with `ffmpeg`
(`PathToFFMPEG`, see [options](../../options)) as h264. A
[camera flight](../../Primitives/camera) is not replayed, the slide's view is
applied directly, as in a [PDF export](../export).


