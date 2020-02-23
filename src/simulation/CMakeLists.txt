cmake_minimum_required(VERSION 3.16)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

project(Simulation)

find_package(OpenGL REQUIRED)

# GLAD settings
set(GLAD_INCLUDE "${PROJECT_SOURCE_DIR}/Dependencies/GLAD/include/")
add_library(GLAD "${PROJECT_SOURCE_DIR}/Dependencies/GLAD/src/glad.c")

# GLFW settings
set(GLFW_INCLUDE "${PROJECT_SOURCE_DIR}/Dependencies/GLFW/include/")
set(GLFW_ROOT "${PROJECT_SOURCE_DIR}/Dependencies/GLFW/src/")

set(GLFW_COMMON_SRC "${GLFW_ROOT}/glfw_config.h"
					"${GLFW_ROOT}/context.c"
					"${GLFW_ROOT}/init.c"
					"${GLFW_ROOT}/input.c"
					"${GLFW_ROOT}/monitor.c"
					"${GLFW_ROOT}/vulkan.c"
					"${GLFW_ROOT}/window.c")

if (WIN32)
	add_library(GLFW ${GLFW_COMMON_SRC}
					"${GLFW_ROOT}/win32_init.c"
					"${GLFW_ROOT}/win32_joystick.c"
					"${GLFW_ROOT}/win32_monitor.c"
					"${GLFW_ROOT}/win32_time.c"
					"${GLFW_ROOT}/win32_thread.c"
					"${GLFW_ROOT}/win32_window.c"
					"${GLFW_ROOT}/wgl_context.c"
					"${GLFW_ROOT}/egl_context.c"
					"${GLFW_ROOT}/osmesa_context.c")
					
	add_compile_definitions("_GLFW_WIN32" "_CRT_SECURE_NO_WARNINGS")
elseif(LINUX OR APPLE)
		add_library(GLFW ${GLFW_COMMON_SRC}
					"${GLFW_ROOT}/x11_init.c"
					"${GLFW_ROOT}/x11_monitor.c"
					"${GLFW_ROOT}/x11_window.c"
					"${GLFW_ROOT}/xkb_unicode.c"
					"${GLFW_ROOT}/posix_time.c"
					"${GLFW_ROOT}/posix_thread.c"
					"${GLFW_ROOT}/glx_context.c"
					"${GLFW_ROOT}/egl_context.c"
					"${GLFW_ROOT}/osmesa_context.c"
					"${GLFW_ROOT}/linux_joystick.c")
					
		add_compile_definitions("_GLFW_X11")
endif()

# Main project settings
set(SIMULATION_ROOT "${PROJECT_SOURCE_DIR}/Simulation/src/")

file(GLOB_RECURSE SUB_SOURCES
					"${SIMULATION_ROOT}/*.cpp"
					"${SIMULATION_ROOT}/*.h")

include_directories("${SIMULATION_ROOT}"
					"${PROJECT_SOURCE_DIR}/Dependencies/glm/glm/"
					${GLAD_INCLUDE}
					${GLFW_INCLUDE}
)

add_executable(Simulation ${SUB_SOURCES})
target_link_libraries(${PROJECT_NAME} GLAD GLFW opengl32)

set_target_properties(Simulation PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE "${PROJECT_SOURCE_DIR}/")
set_target_properties(Simulation PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG "${PROJECT_SOURCE_DIR}/")

add_compile_definitions("COMPILE_PATH_OFFSET=\"./Simulation\"")