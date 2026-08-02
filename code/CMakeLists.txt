cmake_minimum_required(VERSION 3.14)
project(slope_doc_examples LANGUAGES CXX)

# Pulls slope straight from GitHub (which in turn CPM-fetches polyscope,
# eigen, spdlog, fmt, yaml-cpp on its own) so these examples build against
# whatever is currently on the public repo's main branch.
include(FetchContent)
FetchContent_Declare(
  slope
  GIT_REPOSITORY https://github.com/baptiste-genest/slope.git
  GIT_TAG main
)
FetchContent_MakeAvailable(slope)

add_subdirectory(shader_basics)
add_subdirectory(shader_multipass)
add_subdirectory(shader_scene)
add_subdirectory(shader_advanced)
add_subdirectory(shader_io)
