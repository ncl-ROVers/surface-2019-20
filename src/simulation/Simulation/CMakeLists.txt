project(Simulation)

set(SIMULATION_ROOT "./src/")

macro(GroupSources curdir)
	file(GLOB children RELATIVE ${PROJECT_SOURCE_DIR}/${curdir} ${PROJECT_SOURCE_DIR}/${curdir}/*)
	foreach(child ${children})
		if(IS_DIRECTORY ${PROJECT_SOURCE_DIR}/${curdir}/${child})
			GroupSources(${curdir}/${child})
		else()
			string(REPLACE "/" "\\" groupname ${curdir})
			
			source_group(${groupname} FILES ${PROJECT_SOURCE_DIR}/${curdir}/${child})
		endif()
	endforeach()
endmacro()

GroupSources(src)

file(GLOB_RECURSE SUB_SOURCES
					"${SIMULATION_ROOT}/*.cpp"
					"${SIMULATION_ROOT}/*.h")

include_directories("${SIMULATION_ROOT}"
					"../Dependencies/glm/glm/")

add_executable(Simulation ${SUB_SOURCES})
target_link_libraries(Simulation GLAD GLFW opengl32 TurboJPEG)

add_custom_command(TARGET Simulation PRE_BUILD
				   COMMAND python ARGS ${CMAKE_SOURCE_DIR}/Scripts/build_turbojpeg.py
				   BYPRODUCTS jpeg jpeg-static turbojpeg turbojpeg-static)

# set_target_properties(Simulation PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE "${PROJECT_SOURCE_DIR}/build1")
# set_target_properties(Simulation PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG "${PROJECT_SOURCE_DIR}/build")

add_compile_definitions("COMPILE_PATH_OFFSET=\"../../Simulation\"")