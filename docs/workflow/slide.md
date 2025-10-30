---
title: Slide management 
---

The way the user adds elements to the slides is with streams ```<<```

The core object is the ```Slideshow``` object that must be unique for each presentation.

### Adding elements

Adding elements to the current slide is simply:
``` c++
    Slideshow show;
    show << Mesh::Add("bunny.obj");
```

### Sequencing

If you want elements to appear not all at the same time, you must use ```inNextFrame```:

``` c++
    show << Mesh::Add("bunny.obj");
    show << inNextFrame << Latex::Add("A bunny")->at("bunny"); // will appear in the next slide
```

If you want to remove an object in the next slide, you can use ```>>```:
``` c++
    auto bunny = Mesh::Add("bunny.obj");
    show << Title("The bunny disappears!")->at(TOP) << bunny;
    show << inNextFrame >> bunny; // Title remains but bunny fades away ;-(
```


### New slide

To switch to the next slide, you must use ```newFrame```:

``` c++
    show << Title("My first slide")->at(CENTER);  
    show << PointCloud::Add(X);
    show << newFrame << Title("My second slide")->at(TOP); // new slide only contains new title
```
