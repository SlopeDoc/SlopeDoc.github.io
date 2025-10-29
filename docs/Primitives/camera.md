---
title: Camera placement
---

Just as for text, setting the camera programmatically would be very unpleasant. Hence, when creating your slides, one can save at any time the current 
state of the camera, by pressing ```C```, under a key name (must be unique), which can then be loaded in the code:

<video src="../../static/save_cam.mp4" muted autoplay loop controls width="100%" >
</video>

```c++ title="Loading a camera"
    show << CameraView::Add("bunny");

```

??? note "Fly To animation"
    Pretty transitions between cameras is possible using the FlyTo options:
    
    ``` c++ 
        CameraView::Add(std::string key,bool flyTo = false)
    ```

