---
title: Titles
---

As titles are a special kind of text, you can use the ```Title(std::string text)``` wrapper, it create a latex object that is larger by default and is *unique*: if a new title is added to a slide it will replace the previous one.
``` c++
    show << Title("This is a title");
    // add some stuff
    show << inNextFrame << Title("This is the new title"); //everything is copied but the title is replaced
    show << newFrameSameTitle;// everything is removed execpt the title 

```
