--- 
title: Absolute
---

The simplest way to place a screen primitive in a slide is through absolute placement (expressed in relative coordinates):
``` c++
    // place at half of the width and 20% of the height, from the bottom-left
    show << Image::Add("dog.png")->at(0.5,0.2); 
```

For common positions, many wrappers exist:

```c++
    show << Title("absolute")->at(TOP); // also exist with CENTER and BOTTOM
    show << PlaceLeft(ptr,y_coord,offset); 
    show << PlaceRight(ptr,y_coord,offset); 
    show << PlaceBottom(ptr,x_coord,offset); 
    show << PlaceTop(ptr,x_coord,offset); 
```
