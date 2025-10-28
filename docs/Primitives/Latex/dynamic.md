---
title: Hot Reloading
---

```json title="latex.json"
{
"key1":[0,"Some text",1],
"key2":[1,"\pi \approx 3",1]
}

```

In the code:
```c++
LatexLoader::Init("latex.json");

show << LatexLoader::Load("key1");

// equivalent to LatexLoader::Load("key2")->at("key2")
show << LatexLoader::LoadWithKey("key2");  
```

