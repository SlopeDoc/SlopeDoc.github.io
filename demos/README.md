# Demos

One small slope deck per documented feature. `render.sh` builds them and records
each to `docs/static/<name>.mp4` with slope's `--record`, so the videos in the
docs are reproducible rather than hand-captured.

## Layout

```
demos/
  CMakeLists.txt      one executable per feature, slope pulled by FetchContent
  render.sh           build + record all demos into docs/static/
  code/               the Code primitive  ->  docs/static/code.mp4
    main.cpp
    newton.py         the listing it walks through
    views/            label position + tuned colours, so a render is stable
```

## Rendering

```
./render.sh
```

pulls slope from `github.com/baptiste-genest/slope@main` (which must carry the
`--record` flag). To try an unreleased build:

```
./render.sh -DSLOPE_SOURCE_DIR=/path/to/slope
```

`RES`, `FPS` and `BUILD` are environment overrides. Frames are staged in
`/tmp/slope_record_<name>/` and the `.mp4` lands in `docs/static/`.

## Adding a demo

1. `demos/<name>/main.cpp` — `show.init("<name>", ...)`, a short deck, `show.run()`.
2. place text at labels, commit a `views/*.pos` so the render does not depend on
   the Tuner.
3. `add_subdirectory(<name>)` in `demos/CMakeLists.txt`, a `CMakeLists.txt` next
   to the source, and a `render <exe> <name> <name>` line in `render.sh`.
4. embed `static/<name>.mp4` from the matching docs page.
