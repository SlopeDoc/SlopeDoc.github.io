---
title: Keyboard shortcuts
---

While a presentation is running, Slope reacts to the keys below. You can also print this list in the terminal by launching your executable with ``--help``.

### Navigation

| Key | Action |
| --- | --- |
| ``→`` right arrow | Next slide, or start the slide's [timed pause](../workflow/pause) if it has one |
| ``←`` left arrow | Previous slide |
| ``↓`` down arrow | Skip to the next slide **without** transition |
| ``Tab`` | Slide menu: jump to any slide and read [rehearsal timings](timings) |

### Interactive placement

These act on [persistent screen primitives](../placement/persistant_placement).

| Key / mouse | Action |
| --- | --- |
| ``Ctrl`` + left click | Pick the primitive under the cursor; click again on the same spot to cycle down through primitives stacked there |
| drag | Move the picked primitive (light-blue guides snap it to other primitives) |
| mouse wheel | Scale the picked primitive |
| ``H`` | Center it horizontally |
| ``V`` | Center it vertically |
| ``Ctrl`` + ``Shift`` + left click | Toggle the primitive in/out of a group selection |
| ``Ctrl`` + ``Shift`` + drag | Marquee selection: every primitive entirely enclosed by the box joins the group |
| left drag (with a group selected) | Move the whole group, preserving relative spacing (a short click clears the selection) |
| ``Ctrl`` + ``Z`` | Undo the last move |
| ``Ctrl`` + ``S`` | Save all dragged positions and edited [parameters](../interactivity) to disk |
| ``T`` | Transform guizmo editor (3D objects) |

### Tools & windows

| Key | Action |
| --- | --- |
| ``C`` | Export the current camera view |
| ``W`` | Color palette editor |
| ``D`` | Polyscope GUI |
| ``L`` | Reload LaTeX (hot reload) |
| ``A`` | Tuner panel: [tunable parameters](../interactivity) of the current slide, and their handles |
| ``P`` | Screenshot (saved to ``/tmp/screenshot_*.png``) |
| ``R`` | Reset [rehearsal timings](timings) |
| ``Space`` | Pause/resume the rehearsal timer |
