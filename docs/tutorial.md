---
title: Step by step example
---

Let's create a simple set of slides to demonstrate the common use, and good practices, of the library.

## Simple template

A simple & clean template for a project could be like this:
``` c++
#include "slope.h"

using namespace slope;
Slideshow show;


void init () {
    Latex::UsePackage("libertine"); // set font
    LatexLoader::Init("text.json"); // set latex source

}

int main(int argc,char** argv) {
    show.init("A simple project",argc,argv);
    init();
    show.run();
    return 0;
}
```
We use ```Latex::UsePackage``` to append before all latex files the *libertine* package to set the font for the text and formulas and ```LatexLoader::Init("text.json)``` to indicate the file for the [hot reloading](../Primtitives/Latex/dynamic.md) of the text. Even for simple text, assume that you will have to edit the text many times so using the hot-reloading is always a good idea.

Note that a good idea to reduce compilation time would be to generate each group of slides in different cpp files to avoid recompiling everything at each edits, but let's do everything in one block for the sake of clarity.


## Titles

[Titles](../Primitives/Latex/titles) are essential in a presentation and in slope they allow to label each group of slides to enable jumping back and forth between slide groups. They appear larger than standard text and are unique to a slide. Let's make it appear at the center first, and then make it move to the top at the next slide.

``` c++
    show << Title("The moon and the tides")->at(CENTER);
    show << inNextFrame << TOP;
```

Note that only adding ```TOP``` will refer automatically to the last primitive inserted. Here it is equivalent to:

``` c++
    auto title = Title("The moon and the tides");
    show << title->at(CENTER);
    show << inNextFrame << title->at(TOP);
```

## Primitives and camera

The core objects in slope are the primitives, that are either [screen ones](Primitives/screen_primitives.md) (purely in 2D space in the screen), or [Polyscope ones](Primitives/polyscope_primitives.md), we can start by adding a sphere:

``` c++
    // adding a mesh
    auto planet = Mesh::Add("sphere.obj");
    show << planet;
    planet->pc->setSurfaceColor(glm::vec3(0.5,0.6,1));
```

At this point, you should get this:
<video src="../static/tuto1.mp4" muted autoplay loop controls width="100%" >
</video>

We first adapt the camera to the scene by changing it as usual with polyscope and you can save the view by pressing ```c``` and here we save it under ```view1``` and add it to the scene:
``` c++
    show << CameraView::Add("view1");
```

## Text and hot-reloading

We can also start adding text, do it by modifing the latex souce file, here ```test.json```:
=== "main.cpp"
    ``` cpp
        show << LatexLoader::LoadWithAnchor("moon1");
    ```
=== "text.json"
    ```json
    {
        "moon1":[0,"The moon is essentialy a very big rock"]
    }
    ```

We can hot-reload the text (and its width) in the json file, and we can move (and scale) the text as we loaded it with a [(persistent) anchor](Primitives/placement/persistant_placement.md).

<video src="../static/tuto2.mp4" muted autoplay loop controls width="100%" >
</video>

## Animations and screen space tracking

We can add a point that follows a simple trajectory:
```cpp 
    auto moon = Point::Add([] (TimeObject t) -> vec {
        float angle = t.inner_time;
        scalar r = 1.3;
        return r*vec(cos(angle), sin(angle), 0);
    });
    show << moon;
``` 
And a text label that follows the point:
```cpp 
    show << Latex::Add("The moon")->track([moon] () {return moon->getCurrentPos();}, vec2(0,-0.05));
```

## Polyscope quantities

We can also make a scalar field appear at a different moment than the mesh itself, and access to its own polyscope attributes:

```cpp
    Vec tide = Vec::Zero(planet->getVertices().size());
    auto q = planet->pc->addVertexScalarQuantity("tide",tide);
    auto tide_plot = PolyscopeQuantity<polyscope::SurfaceVertexScalarQuantity>::Add(q);
    tide_plot->q->setColorMap("blues");
```

A simple yet powerful animation idea is to update the scalar values and the mesh itself in a single updater:

```cpp
    auto verts = planet->getVertices();

    tide_plot->updater = [verts,planet,q,tide,moon](TimeObject t){
        Vec values = tide;
        vec m = moon->getCurrentPos();
        auto new_pos = verts;
        for (size_t i = 0; i < planet->getVertices().size(); i++) {
            values(i) = 1/(verts[i] - m).squaredNorm();
            new_pos[i] += 0.01*values(i)*verts[i];// offset sphere in normal direction
        }
        q->updateData(values);
        q->setMapRange({values.minCoeff(),values.maxCoeff()}); //required for polyscope to update
        planet->updateMesh(new_pos);
    };

    show << tide_plot;
```

<video src="../static/tuto3.mp4" muted autoplay loop controls width="100%" >
</video>

Overall pretty simple right?

# Full code

```cpp
#include "slope.h"

using namespace slope;
Slideshow show;


void init () {
    Latex::UsePackage("libertine"); // set font
    LatexLoader::Init("test.json"); // set latex source

    show << Title("The moon and the tides")->at(CENTER);
    show << inNextFrame << TOP;

    auto planet = Mesh::Add("sphere.obj");
    show << planet;
    planet->pc->setSurfaceColor(glm::vec3(0.5,0.6,1));


    show << CameraView::Add("base");

    show << LatexLoader::LoadWithAnchor("moon1");


    show << inNextFrame;

    auto moon = Point::Add([] (TimeObject t) -> vec {
        float angle = t.inner_time;
        scalar r = 1.3;
        return r*vec(cos(angle), sin(angle), 0);
    });

    show << moon;
    show << Latex::Add("The moon")->track([moon] () {return moon->getCurrentPos();}, vec2(0,-0.05));

    Vec tide = Vec::Random(planet->getVertices().size());
    auto q = planet->pc->addVertexScalarQuantity("tide",tide);
    auto tide_plot = AddPolyscopeQuantity(q);

    auto verts = planet->getVertices();
    tide_plot->q->setColorMap("blues");

    tide_plot->updater = [verts,planet,q,tide,moon](TimeObject t){
        Vec values = tide;
        vec m = moon->getCurrentPos();
        auto new_pos = verts;
        for (size_t i = 0; i < planet->getVertices().size(); i++) {
            values(i) = 1/(verts[i] - m).squaredNorm();
            new_pos[i] += 0.01*values(i)*verts[i];// offset sphere in normal direction
        }
        q->updateData(values);
        q->setMapRange({values.minCoeff(),values.maxCoeff()}); // required for polyscope to update
        planet->updateMesh(new_pos);
    };

    show << tide_plot;

    show << newFrame;
    // make more slides here!
}

int main(int argc,char** argv) {
    show.init("A simple project",argc,argv);
    init();
    show.run();
    return 0;
}

```