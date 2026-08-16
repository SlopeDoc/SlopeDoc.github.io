The way animations can be programmatically conceived is through updaters.

All primitives have an updater object that is called at each frame such that each primitive can be time-dependent. It takes a `TimeObject`, which carries the clocks, the current slide and the keyframe queries described below.

An updater is C++, so editing one costs a rebuild. The constants it reads belong in a [parameter](../../live/params), and often the motion itself belongs in a [snippet](../../live/snippets); both are re-read on save, and both expose the same queries.

```cpp
auto pc = PointCloud::Add(positions);
pc->updater = [pc] (TimeObject t) {

    if (t.relative_frame_number == 0) {
        auto P = pc->getPoints();
        for (auto& x : P) 
            x(0) += std::sin(t.inner_time);
        pc->updateCloud(P);
    } else if (t.relative_frame_number == 1) {
        // do something else
    }
};
```

Inserting a slide shifts every branch written this way. Two alternatives avoid frame numbers.

An updater can be replaced starting at another frame, so each behavior is written where it begins rather than selected by a number:

```cpp
auto pc = PointCloud::Add(positions);
pc->updater = [pc] (TimeObject t) {
    // default behavior
};
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
    - ```inner_time``` (s) : time from first appearance on screen
    - ```absolute_frame_number``` (int) : current frame number from first slide
    - ```relative_frame_number``` (int) : number of slides from first appearance of this primitive
    - ```transition_parameter``` : 0 to 1 across a slide change, 1 once settled

    The same fields reach [shaders as uniforms](../Shader/basics#following-the-talk) and [snippets](../../live/snippets#what-t-gives-you) under the same names.

## Keyframes

Branching on frame numbers breaks as soon as slides are inserted or reordered. Label the relevant frame while composing the show and test it by name:

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

### Counting from a keyframe

A boolean switches but cannot ease. Two queries measure the distance from a keyframe:

```cpp
int stage = std::clamp(t.slidesSinceKeyframe("build"), 0, 3);   // in slides
scalar a  = smoothstep(t.secondsSinceKeyframe("wobble") / 0.8); // in seconds
```

- ```t.slidesSinceKeyframe("label")``` : negative before the keyframe, 0 on it. An unreached label answers a large negative value, so the usual `>= n` tests stay false like `afterKeyframe`.
- ```t.secondsSinceKeyframe("label")``` : seconds since that keyframe was **reached**, the clock an ease wants. `from_action` restarts on every slide change, even an unrelated one, so easing on it snaps back. Never negative, and 0 before the keyframe, so an ease needs no guard.

### Blending states helper

```duringKeyframe``` is a weight: 0, rising to 1 across the transition **into** its keyframe, 1 while it holds, and falling back to 0 across the transition **out** of it. The ramps are the slide transition itself, so the weights of neighbouring keyframes always sum to 1 and a value can be written as a plain blend of its states:

```cpp
pos = rest * t.duringKeyframe("a") + moved * t.duringKeyframe("b");
```

One name is a single slide, for a window use `t.duringKeyframe("from", "to")` opens the window at `from` and closes it at `to`. Unknown names weigh 0, so if each state is an *offset* from a resting value, the resting state needs no weight of its own.

In a [snippet](../../live/snippets) the three are spelled `t:slidesSince`, `t:secondsSince` and `t:during`.
