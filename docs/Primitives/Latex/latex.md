---
title: Basics
---

In order to add text on your slides, you can add Latex, either by hardcoding it in the program, or by [loading](../dynamic) it from an external source (recommended).

To make things easier between standard text and formulas, two builders exist:

```c++
    show << Latex::Add("Some text, can use math $\\pi$");
    show << Formula::Add("\\int_0^1 t dt = 8"); // math mode by default
```

Importing latex packages can be easily done using:

```c++
    Latex::AddToPrefix("\\usepackage{libertine}"); 
    // will be added before ALL latex objects
```

Latex files are then hashed and stored in a cache to only generate them once.

!!! tip "Full string escape"
    For complex strings, escaping each \ is painful, remember that C++ offers full string escaping:
    ```c++
    Latex::Add(R"( much easier like that : $\pi = \int_0^3 1 dt$ )")    
    ```

!!! note "Image resolution"
    Slope naively converts latex pdf to png, hence we lose the scale invariance of vector graphics. If you want to scale some text to very large you can change the DPI for the conversion, by setting ```slope::Options::PDFtoPNGDensity```.



## Manifest format

Three item keys produce latex, differing only in where the source comes from and
whether it is text mode or math mode:

```yaml
- latex: \emph{inline} latex   # text mode, written here
  scale: 1.2                   # size multiplier (default: 1)
  width: 300                   # wrapping width in pt, where lines break
- formula: e^{i\pi}+1=0        # math mode, written here
- load: my_key                 # from the definitions file, either mode
  at: my_label                 # defaults to a label derived from the key
```

`load:` is the one to prefer: the manifest keeps the structure of the talk and
the [definitions file](../../../deck/getting_started) keeps the prose, so
neither is buried in the other.
