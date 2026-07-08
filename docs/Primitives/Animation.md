The way animations can be programatically conceived is through updaters.

All primitives have an updater object that is called at each frame such that each primitive can be time-dependant:

```cpp
auto pc = PointCloud::Add(positions);
pc->updater = [pc] (TimeObject t) {

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

If you want to avoid having to code each behavior for each relative frame (and be resilient to slide changes), you can replace an updater starting at another frame directly:  

```cpp
auto pc = PointCloud::Add(positions);
pc->updater = [pc] (TimeObject t) {
    // default behavior
}
show << inNextFrame << pc;
// do stuff, create new slides, etc...
show << pc->setUpdater([pc] (TimeObject time){
    // new behavior starting from this frame
});
```


!!! note "```TimeObject```"
    The TimeObject given in parameter of the updater contains all relevant time information for each primitive:

    - ```from_begin``` (s) : time from start of the program
    - ```from_action``` (s) : time from last slide change
    - ```inner_time``` (s) : time from first appearence on screen
    - ```absolute_frame_number``` (int) : current frame number from first slide
    - ```relative_frame_number``` (int) : number of slides from first appearence of this primitive

## Keyframes

Branching on frame numbers breaks as soon as slides are inserted or reordered. Instead, label a frame while composing the show and test it by name in the updater:

```cpp
show << Keyframe("noise_on");
```

```cpp
pc->updater = [pc] (TimeObject t) {
    if (t.afterKeyframe("noise_on")) {
        // ...
    }
};
```

- ```t.afterKeyframe("label")``` : true from the labeled frame on
- ```t.atKeyframe("label")``` : true exactly on the labeled frame
- ```t.beforeKeyframe("label")``` : true strictly before it

An unknown label warns once in the terminal and answers false. In a [deck manifest](../../deck/manifest), the same mark is written `- keyframe: label`.
