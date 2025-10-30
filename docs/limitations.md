---
title: Limitations
---

Before giving it a try, be aware of the following limitations:

- Making slides with Slope can be **very** time consuming, having to recompile at each change takes a lot of time. (Happily, the result if often worth it :wink:)
- Since it is only built on top of [Polyscope](https://polyscope.run), we share its features and its (few) limitations: no multi-view compositing, no shadows, etc...
- Slope is mainly **poorly written**, it was a small side project to give a lecture about differential geometry that turned into my main tool for presentations, but many design patterns are dark ones, so it may impact long term developpement... Feel free to indicate ways to upgrade the code quality or to contribute!
- We also share the general limitations of *litterate programming*, hence combining slides from different talks can be painful if you use scientific code. To alleviate this issue, slope offers ways to import/export data.
- If the conference you are presenting at has the terrible policy of not allowing presentations on your own laptop, or if you want to share your slides, you may turn it into a PDF, but nothing is automatic (yet). You have to manually screenshot each slide (at the time you see fit for the animations), by pressing ```p```, and then concatenate them into a pdf.

