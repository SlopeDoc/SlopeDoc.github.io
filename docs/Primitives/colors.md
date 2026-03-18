Some objects, like the background color, can use a special Color structure:

- Either a fixed rgb code:
```cpp
BackgroundColor::Default = Color(1,0,0); // pure red
```
- Or a reference to a palette that can be changed and stored dynamicaly by pressing ```w```:
```cpp
BackgroundColor::Default = Color("base");
```
<video src="../../static/colors.mp4" muted autoplay loop controls width="100%" >
</video>

