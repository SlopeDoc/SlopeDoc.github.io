---
title: Hot Reloading
---

When creating the slides, text is more often edited than the rest. In order to avoid recompiling, hot reloading of an external source file is possible.

=== "Json LateX source"

    ``` json
    {
    "key1":[0,"Some text",1],
    "key2":[1,"\pi \approx 3",1]
    }
    ```

=== "Code"

    ``` c++
    LatexLoader::Init("latex.json");

    show << LatexLoader::Load("key1");

    // equivalent to LatexLoader::Load("key2")->at("key2")
    show << LatexLoader::LoadWithKey("key2");  
    ```

In the Json, the first element must be 0 or 1, 0 for text, 1 for formulas, the middle one is the content, the last one is the scale of the text.

!!! warning "Warning"
    The reloading occurs when the json file is saved, if there is an error in the LateX, the program will end.
