---
title: Stacks
---

## Vertical stacks

```Stack2D``` lays out screen primitives below one another with uniform spacing, the whole block centered on a single *handle*. The layout is recomputed every frame, so it follows drag edits of the handle and size changes of the children (hot-reloaded latex...).

```c++
auto stack = Stack2D::Add("column");   // label handle : draggable as one unit
show << stack->at("column");

stack->addChild(paragraph1);
show << stack->place(paragraph1);
stack->addChild(paragraph2);
show << inNextFrame << stack->place(paragraph2);  // registered now :
                                                  // space is reserved
```

The layout is computed from **all** registered children, visible or not: a child appearing at a later step fades in at its final position, and earlier children never move.

The stack draws nothing itself; it exists as a screen primitive so that arrows and [englobing boxes](../shapes) can target the whole block.

| Field | Effect |
| --- | --- |
| `spacing` | vertical gap between children, relative units |
| `align` | `LEFT`, `CENTER` or `RIGHT` |
| `handle` | block center; a label makes the block drag-editable |

In a deck manifest, stacks are available as the `stack:` item (see [manifest format](../../deck/manifest)).
