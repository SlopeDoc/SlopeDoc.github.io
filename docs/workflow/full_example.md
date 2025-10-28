---
title: Step by step example
---

Starting only from pure documentation can be hard so here is a step by step example to handle the core concepts of slope!

```c++ title="Project Template" linenums="1"
#include "slope.h"

using namespace slope;

Slideshow show;

void CreateSlides() {


}



int main(int argc,char** argv) {
    show.init("My first slope project",argc,argv);
    CreateSlides();
    show.run();
    return 0;
}

```

