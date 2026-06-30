---
title: Speaker notes
---

Slope can open a **second window** acting as a teleprompter that shows your notes for the slides currently on screen. Keep it on your laptop while the presentation is projected on the main screen.

### Writing a script

Notes live in a plain text file split into tagged blocks. A line of the form ``[tag]`` starts a block, and every following line until the next tag is the note for that tag:

```title="notes.txt"
[intro]
Welcome everyone. Today we talk about bunnies.
Take it slow here.

[results]
Insist on the convergence plot.
```

### Linking notes to slides

Register the file once, then wrap the slides that share a note between a tag and ``ClosePromptTag``:

```c++
    show.setScriptFile("notes.txt"); // path relative to the project folder

    show << promptTag("intro");
    show << Title("Welcome")->at(CENTER);
    show << newFrame; /* ... */
    show << promptTag("results");
    show << newFrame; /* ... */
```

As you move through the slideshow, the prompter window automatically displays the note attached to the current slide's tag.
