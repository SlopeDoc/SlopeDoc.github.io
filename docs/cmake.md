---
title: Build & CMake Integration
---

Slope is designed to be easily integrated on top of any cmake project in order to merge scientific code and your presentations!



=== "In CMakeLists.txt"
    
    ```cmake linenums="1"
    project(slope_project)
    cmake_minimum_required(VERSION 3.5)
        
    list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    
    include(slope)
    
    add_executable(slope_project slides.cpp )
    target_link_libraries(slope_project slope)
    ```
=== "FetchContent file"

    ```cmake title="slope.cmake" linenums="1"
    include(FetchContent)
    FetchContent_Declare(
      slope
      GIT_REPOSITORY https://github.com/baptiste-genest/slope.git
      GIT_TAG v0.1.6
    )
    FetchContent_MakeAvailable(slope)
    ```

### Dependencies
- the same as [Polyscope](https://polyscope.run/about/dependencies/)
- Imagick (```convert``` command) : Make sure that the convert command is allowed to convert pdf to png, see [here](https://stackoverflow.com/a/53180170).
- ```pdflatex```
- ```ffmpeg``` and ```ffprobe```, optional, only for the [Video and Webcam](../Primitives/video) primitives.

[Paths](../options) to Imagick, pdflatex and ffmpeg are found by cmake.

On a Debian or Ubuntu machine, ```ffmpeg``` provides both tools and
```imagemagick``` provides ```convert```:

```
sudo apt install texlive-latex-extra imagemagick ffmpeg
```


### Code syntax highlighting

[Code](../Primitives/code) is highlighted by tree-sitter, which cmake fetches like
the other dependencies. It produces one grammar per language, compiled once (takes roughly 1 minute)

**python, glsl, cpp and yaml** are built by default. `SLOPE_LANGUAGES` trims that list, down
to nothing (code is then drawn as plain text), and `SLOPE_EXTRA_LANGUAGES` adds any
grammar repository carrying a `src/parser.c` and a `queries/highlights.scm`, as
`name|repo|tag|extensions`:

```cmake
set(SLOPE_LANGUAGES python glsl CACHE STRING "")
set(SLOPE_EXTRA_LANGUAGES "rust|tree-sitter/tree-sitter-rust|v0.23.2|rs" CACHE STRING "")
```

Both are cache variables. Set them before the first configure, or pass
`cmake -DSLOPE_LANGUAGES="python;glsl" .` to a build directory that already exists. The
highlight queries are installed alongside the library, under `share/slope/queries`.

### Build and run !

```
mkdir build && cd build
cmake ..
make -j
./exe --project_path /path/to/your/project/folder
```
