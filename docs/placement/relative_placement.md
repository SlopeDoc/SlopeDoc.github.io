---
title: Relative
---

Primitives can be placed with respect to another one. The main way to do so is with:

!!! note "```PlaceRelative(ScreenPrimitivePtr A,ScreenPrimitivePtr other,placeX X,placeY Y,scalar paddingX,scalar paddingY)```"
    - ```ScreenPrimitivePtr A``` primitive to place wrt to B
    - ```ScreenPrimitivePtr other``` reference Primitive
    - ```placeX X``` can be:  ```REL_LEFT, ABS_LEFT, CENTER_X,SAME_X,REL_RIGHT,ABS_RIGHT``` for example ```REL_X``` will place A to the left of B, ```ABS_RIGHT``` will place A to the right of the screen
    - ```placeY Y``` can be:  ```REL_TOP, ABS_TOP, CENTER_Y,SAME_Y,REL_BOTTOM,ABS_BOTTOM```
    - ```scalar paddingX ``` offset in the opposite direction of the placeX in the x-coord
    - ```scalar paddingY ``` offset in the opposite direction of the placeY in the x-coord

!!! info "Dynamic tracking"


    <video 
        src="../../static/relative.mp4" 
        autoplay 
        muted 
        loop 
        style="display: block; float: right; margin-left: auto;margin-bottom: auto; margin-right: auto; width: 200px; height: auto;">
    </video>

    The relative placement is dynamic, if the reference primitive moves, the placement is updated:
    ``` c++
        show << Latex::Add("I'm A")->at("A");
        show << PlaceBelow(Latex::Add("I follow A"),0.03);
    ```

Of course, many wrappers exist over this to simplify stuff for common constructions:

### Wrappers:

??? note "```PlaceNextTo(ScreenPrimitivePtr ptr,int side,scalar paddingx = 0.01,ScreenPrimitivePtr other = nullptr) ```"
    side 0 = left, side 1 = right

!!! note "```PlaceBelow(ScreenPrimitivePtr ptr,ScreenPrimitivePtr other,scalar paddingy = 0.01)```"
!!! note "```PlaceAbove(ScreenPrimitivePtr ptr,ScreenPrimitivePtr other,scalar paddingy = 0.01)```"

!!! tip "**Last primitive inserted**"
    If you don't specify ```other```, then it will use as reference the *last* screen primitive inserted in the slide.
    ```c++
    show << Title("Relative is better")->at(TOP);
    show << PlaceBelow(Latex::Add("sub title"),0.1); // will place below title
    ```
