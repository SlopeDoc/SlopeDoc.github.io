---
title: Colors
---

Anywhere Slope asks for a color, you can give it a fixed one:

```cpp
show << Background(0.1, 0.1, 0.12);
```

or a name, and then it becomes something you can edit live:

```cpp
show << Background("bg");
box->color = Color("shape/clay");
```

A named color is a [tunable parameter](../../live/params) like any other. It shows up in the Tuner (```A```).

Because it is one namespace, a color can also be read from a [snippet](../../live/snippets) by its name, or bound to a shader uniform. You can define a snippet to override a color:

```lua title="snippets.lua"
--- shape/clay
local h = 0.5 + 0.5 * math.sin(t.from_begin)
return vec4(h, 0.3, 1 - h, 1)
```

## Background

The background is an important part of a slide. If you set it on a slide, every slide after it keeps it, until another one changes it.

```cpp
show << Background("bg");        // a named color, tuned live
show << Background(1, 1, 1);     // or a literal
```

```yaml title="deck.yaml"
- background: bg
- background: [0.05, 0.05, 0.08]
```
