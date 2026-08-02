add_executable(shader_multipass main.cpp)
target_link_libraries(shader_multipass PRIVATE slope)

add_custom_command(TARGET shader_multipass POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_CURRENT_SOURCE_DIR}/sim.frag
            ${CMAKE_CURRENT_SOURCE_DIR}/colorize.frag
            $<TARGET_FILE_DIR:shader_multipass>)
