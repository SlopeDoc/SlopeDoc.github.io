---
title: CMake Integration
---

Slope is designed to be easilty integration on top of any cmake project in order to be able to merge scientific code and your presentations!



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
      GIT_TAG main
    )
    FetchContent_MakeAvailable(slope)
    ```

