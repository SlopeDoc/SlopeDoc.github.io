add_executable(shader_scene main.cpp)
target_link_libraries(shader_scene PRIVATE slope)

add_custom_command(TARGET shader_scene POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_CURRENT_SOURCE_DIR}/occluded.frag
            ${CMAKE_CURRENT_SOURCE_DIR}/spot.obj
            $<TARGET_FILE_DIR:shader_scene>)
