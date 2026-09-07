cmake_minimum_required(VERSION 3.14)
project(slope_doc_demos LANGUAGES CXX)

# One executable per documented feature, each recorded to docs/static/<name>.mp4
# by render.sh (slope's --record). slope is pulled from the public repo by
# default; point SLOPE_SOURCE_DIR at a local checkout to try an unreleased build.
set(SLOPE_REPO "https://github.com/baptiste-genest/slope.git" CACHE STRING "slope git remote")
set(SLOPE_TAG  "main" CACHE STRING "slope git ref")
set(SLOPE_SOURCE_DIR "" CACHE PATH "local slope checkout, overrides SLOPE_REPO/SLOPE_TAG")

include(FetchContent)
if(SLOPE_SOURCE_DIR)
  FetchContent_Declare(slope SOURCE_DIR "${SLOPE_SOURCE_DIR}")
else()
  FetchContent_Declare(slope GIT_REPOSITORY "${SLOPE_REPO}" GIT_TAG "${SLOPE_TAG}")
endif()
FetchContent_MakeAvailable(slope)

add_subdirectory(code)
add_subdirectory(plots)
