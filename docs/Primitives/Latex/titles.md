---
title: Titles
---

As titles are a special kind of text, you can use the ```Title(std::string text)``` wrapper, it creates a (special) latex object that is larger by default and is *unique*: if a new title is added to a slide it will replace the previous one.
``` c++
    show << Title("This is a title");
    // add some stuff
    show << inNextFrame << Title("This is the new title"); //everything is copied but the title is replaced
    show << newFrameSameTitle;// everything is removed except the title 

```

### Table of contents

As titles are unique, you can use them to jump between slides: by pressing ```tab``` you get the list of all titles and clicking on one will make you jump directly to the first slide with this title, useful for questions during presentations!

It is then good practice that each slide has a title (or else it will appear in the table of contents as its slide number).
