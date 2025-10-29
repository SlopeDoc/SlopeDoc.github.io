The way animations can be programatically conceived is through updaters.

Each primitive has as updater object that is called at each frame such that each primitive can be time-dependant:

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


!!! note "```TimeObject```"
    The TimeObject given in parameter of the updater contains all relevant time information for each primitive:

    - from_begin (s) : time from start of the program
    - from_action (s) : time from last slide change
    - inner_time (s) : time from first appearence on screen
    - absolute_frame_number (int) : current frame number from first slide
    - relative_frame_number (int) : number of slides from first appearence of this primitive
