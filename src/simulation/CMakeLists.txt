cmake_minimum_required(VERSION 3.16)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

project(ROVSimulation)

find_package(OpenGL REQUIRED)

# TurboJPEG settings
add_library(TurboJPEG INTERFACE)

target_include_directories(TurboJPEG INTERFACE "${CMAKE_SOURCE_DIR}/Dependencies/TurboJPEG/install/include")
if(WIN32)
	target_link_libraries(TurboJPEG INTERFACE "${CMAKE_SOURCE_DIR}/Dependencies/TurboJPEG/install/lib/turbojpeg-static.lib")
elseif(APPLE)
	target_link_libraries(TurboJPEG INTERFACE "${CMAKE_SOURCE_DIR}/Dependencies/TurboJPEG/install/lib/turbojpeg-static.so")
elseif(UNIX)
	target_link_libraries(TurboJPEG INTERFACE "${CMAKE_SOURCE_DIR}/Dependencies/TurboJPEG/install/lib/turbojpeg-static.a")
endif()

# GLAD settings
set(GLAD_INCLUDE "${CMAKE_SOURCE_DIR}/Dependencies/GLAD/include/")
add_library(GLAD "${CMAKE_SOURCE_DIR}/Dependencies/GLAD/src/glad.c" ${GLAD_INCLUDE})
target_include_directories(GLAD PUBLIC ${GLAD_INCLUDE}) 

# GLFW settings
set(GLFW_INCLUDE "${CMAKE_SOURCE_DIR}/Dependencies/GLFW/include/")
set(GLFW_ROOT "${CMAKE_SOURCE_DIR}/Dependencies/GLFW/src/")

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

target_include_directories(GLFW PUBLIC ${GLFW_INCLUDE})

# Main project settings
add_subdirectory(Simulation)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)
