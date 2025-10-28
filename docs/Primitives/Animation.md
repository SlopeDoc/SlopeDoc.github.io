The code way animations can be implemented is through the concept of the updater.

Each primitive has as updater object that is called at each frame such that all the primitives can be time-dependant:

```cpp
auto pc = PointCloud::Add(positions);
pc->updater = [pc] (TimeObject t,Primitive*) {

    if (t.relative_frame == 0) {
        auto P = pc->getPoints();
        for (auto& x : P) 
            x(0) += std::sin(t.inner_time);
        pc->updateCloud(P);
    } else if (t.relative_frame == 1) {
        // do something else
    }
}
```

The TimeObject carries all time information:

- from_begin (s) : time from start of the program
- from_action (s) : time from last slide change
- inner_time (s) : time from first appearence on screen
- absolute_frame_number (int) : current frame number
- relative_frame_number (int) : number of frames from first appearence
