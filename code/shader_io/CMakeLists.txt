add_executable(shader_io main.cpp)
target_link_libraries(shader_io PRIVATE slope)

add_custom_command(TARGET shader_io POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_CURRENT_SOURCE_DIR}/sim.frag
            ${CMAKE_CURRENT_SOURCE_DIR}/view.frag
            $<TARGET_FILE_DIR:shader_io>)
