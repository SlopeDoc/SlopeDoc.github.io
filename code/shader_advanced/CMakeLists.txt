add_executable(shader_advanced main.cpp)
target_link_libraries(shader_advanced PRIVATE slope)

add_custom_command(TARGET shader_advanced POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_CURRENT_SOURCE_DIR}/mrt.frag
            ${CMAKE_CURRENT_SOURCE_DIR}/field.frag
            ${CMAKE_CURRENT_SOURCE_DIR}/compute.frag
            $<TARGET_FILE_DIR:shader_advanced>)
