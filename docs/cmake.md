---
title: Build & CMake Integration
---

Slope is designed to be easilty integrated on top of any cmake project in order to merge scientific code and your presentations!



=== "In CMakeLists.txt"
    
    ```cmake linenums="1"
    project(slope_project)
    cmake_minimum_required(VERSION 3.12)
        
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
      GIT_TAG alpha-0.0.1
    )
    FetchContent_MakeAvailable(slope)
    ```

### Dependencies
- the same as [Polyscope](https://polyscope.run/about/dependencies/)
- Imagick (```convert``` command)
- ```pdflatex```

[Paths](../options) to Imagick and pdflatex are found by cmake.

### Build and run !

```
mkdir build && cd build
cmake ..
make -j
./exe --project_path /path/to/your/project/folder
```
