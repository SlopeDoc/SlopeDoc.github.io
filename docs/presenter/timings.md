---
title: Rehearsal timings
---

Slope can time your run-through so you can check the length of your talk. This is opt-in, through the ``--rehearse`` flag:

```
./project_exe --project_path /home/.../slope_project --rehearse
```

Without it there is no timing overhead, and nothing is read from or written to disk.

Time is accumulated **per section**, where a section is a run of consecutive slides that share the same title. Open the slide menu with ``Tab`` to see the time spent in each section together with the running total.

Press ``R`` at any time to reset all timings, and ``Space`` to pause/resume the timer, so a break doesn't get billed to whatever section you stopped on.

Once a run has been saved, its total and per-section timings are shown live in the ``Tab`` menu next to the current run, along with the delta between the two, so you can see whether you're running ahead of or behind your reference.

!!! note
    Timings are only written to ``views/timings.json`` when you quit through the confirmation popup and pick "Save and quit". Closing without saving (or discarding) never overwrites the previous run's reference numbers.
