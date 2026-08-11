---
title: Boxes
---

### Fixed Box

### Englobing Box
## Manifest format

A `box:` holds items rather than taking a position, it draws a rectangle around
them and follows them as they move.

```yaml
- box:
    - latex: framed content
    - image: fig.png
  padding: 0.02         # margin around the contents, also padx / pady
  color: "#333333"      # the outline
  thickness: 2
  filled: true          # also fill_color, alpha
  id: my_box            # so operations can refer to the box itself
```
