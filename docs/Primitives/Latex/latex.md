---
title: Basics
---

In order to add text on your slides, you can add Latex, either by hardcoding it in the program, or by [loading](../dynamic) it from an external source (recommended).

To make things easier between standard text and formulas, two builders exist:

```c++
    show << Latex::Add("Some text, can use math $\\pi$"); // must escape caracters

    show << Formula::Add("\\int_0^1 t dt = 8"); // math mode by default
```

Importing latex packages can be easily done using:

```c++
    Latex::AddToPrefix("\\usepackage{libertine}"); // will apply to all
```

Latex files are then hashed and stored in a cache to only generate them once.

!!! tip "Full string escape"
    For complex strings, escaping each \ is painfull, remember that C++ offers full string escaping:
    ```c++
    Latex::Add(R"( much easier like that : $ \pi = 3$ )")    
    ```
