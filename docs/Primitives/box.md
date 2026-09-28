---
title: Boxes
---

### Fixed Box

### Englobing Box
## Deck format

A `box:` holds items rather than taking a position, it draws a rectangle around
them and follows them as they move.

```yaml
- box:
    - latex: framed content
    - image: fig.png
  padding: 0.02         # margin around the contents, also padx / pady
  pad_top: 0.06         # one side only, also pad_bot / pad_left / pad_right
  color: "#333333"      # the outline
  thickness: 2
  filled: true          # also fill_color, alpha
  id: my_box            # so operations can refer to the box itself
```
