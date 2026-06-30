---
title: Hot Reloading
---

When creating the slides, text is more often edited than the rest. In order to avoid recompiling, hot reloading of an external source file is possible.

=== "Json LateX source"

    ``` json
    {
    "key1":[0,"Some text"],
    "key2":[1,"\pi \approx 3",80]
    }
    ```

=== "Code"

    ``` c++
    LatexLoader::Init("latex.json");

    show << LatexLoader::Load("key1");

    // equivalent to LatexLoader::Load("key2")->at("key2")
    show << LatexLoader::LoadWithKey("key2");  
    ```

In the Json, the first element must be 0 or 1, 0 for text, 1 for formulas, the middle one is the content, the last one is optional and is the width of the column before linebreak (in pt units).

<video width="100%" autoplay loop muted>
  <source src="../../../static/hot_reload.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
