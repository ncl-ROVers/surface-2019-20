cmake_minimum_required(VERSION 3.3.2)

project(cstreaming LANGUAGES C CXX VERSION 1.0.0)

add_subdirectory(external)
add_subdirectory(external/pybind11)

pybind11_add_module(cstreaming main.cpp)

set_target_properties(cstreaming PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/lib")
set_target_properties(cstreaming PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE "${PROJECT_SOURCE_DIR}/lib")
set_target_properties(cstreaming PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG "${PROJECT_SOURCE_DIR}/lib")

include_directories(${CMAKE_BINARY_DIR}/external/libde265 ${PROJECT_SOURCE_DIR}/external/libde265/)
target_link_libraries(cstreaming PRIVATE libde265)