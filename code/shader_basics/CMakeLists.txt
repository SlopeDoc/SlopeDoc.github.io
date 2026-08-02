add_executable(shader_basics main.cpp)
target_link_libraries(shader_basics PRIVATE slope)

# assets next to the built binary, so `--project_path .` works from there.
# A build-time step, not file(COPY) at configure time, so editing a .frag and
# rebuilding (no reconfigure) picks up the change.
add_custom_command(TARGET shader_basics POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_CURRENT_SOURCE_DIR}/plasma.frag $<TARGET_FILE_DIR:shader_basics>)
