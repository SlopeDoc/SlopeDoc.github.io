include("/home/eulerson314/dev/slope/cmake/CPM.cmake")
CPMAddPackage("NAME;yaml-cpp;GIT_REPOSITORY;https://github.com/jbeder/yaml-cpp.git;GIT_TAG;0.8.0;OPTIONS;YAML_CPP_BUILD_TESTS OFF;YAML_CPP_BUILD_TOOLS OFF;YAML_CPP_BUILD_CONTRIB OFF")
set(yaml-cpp_FOUND TRUE)