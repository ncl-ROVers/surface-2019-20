cmake_minimum_required (VERSION 3.3.2)

project(libde265
    LANGUAGES C CXX
    VERSION 1.0.5
)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# The version number.
set(NUMERIC_VERSION 0x01000500)
set(PACKAGE_VERSION ${PROJECT_VERSION})

include(${CMAKE_ROOT}/Modules/CheckCCompilerFlag.cmake)
include(${CMAKE_ROOT}/Modules/CheckIncludeFile.cmake)

include(GNUInstallDirs)
include(CheckFunctionExists)

find_package(SDL)
find_package(Threads REQUIRED)

CHECK_INCLUDE_FILE(malloc.h HAVE_MALLOC_H)
CHECK_INCLUDE_FILE(stdint.h HAVE_STDINT_H)
CHECK_INCLUDE_FILE(stdbool.h HAVE_STDBOOL_H)
CHECK_FUNCTION_EXISTS(posix_memalign HAVE_POSIX_MEMALIGN)

if (HAVE_MALLOC_H)
  add_definitions(-DHAVE_MALLOC_H)
endif()
if (HAVE_STDINT_H)
  add_definitions(-DHAVE_STDINT_H)
endif()
if (HAVE_STDBOOL_H)
  add_definitions(-DHAVE_STDBOOL_H)
endif()
if (HAVE_POSIX_MEMALIGN)
  add_definitions(-DHAVE_POSIX_MEMALIGN)
endif()

set(LIB_SOURCE libde265/libde265/)
configure_file(${LIB_SOURCE}/de265-version.h.in ${LIB_SOURCE}/de265-version.h)

if(CMAKE_COMPILER_IS_GNUCXX OR ${CMAKE_CXX_COMPILER_ID} MATCHES Clang)
  add_definitions(-Wall)
endif()

option(DISABLE_SSE "Disable SSE optimizations")
if(NOT ${DISABLE_SSE} EQUAL OFF)
  if(MSVC)
    set(SUPPORTS_SSE4_1 1)
  else()
    CHECK_C_COMPILER_FLAG(-msse4.1 SUPPORTS_SSE4_1)
  endif()
endif()

include_directories("${PROJECT_BINARY_DIR}")
include_directories("${PROJECT_SOURCE_DIR}/libde265")
include_directories("${PROJECT_SOURCE_DIR}/libde265/libde265")
if(MSVC)
  include_directories("${PROJECT_SOURCE_DIR}/libde265/extra")
  add_definitions(-DHAVE_STDINT_H)
  add_definitions(-DHAVE_STDBOOL_H)
endif()

# Define libde265 library
include(CMakePackageConfigHelpers)

set(libde265_sources 
  ${LIB_SOURCE}/alloc_pool.cc
  ${LIB_SOURCE}/bitstream.cc
  ${LIB_SOURCE}/cabac.cc
  ${LIB_SOURCE}/configparam.cc
  ${LIB_SOURCE}/contextmodel.cc
  ${LIB_SOURCE}/de265.cc
  ${LIB_SOURCE}/deblock.cc
  ${LIB_SOURCE}/decctx.cc
  ${LIB_SOURCE}/dpb.cc
  ${LIB_SOURCE}/en265.cc
  ${LIB_SOURCE}/fallback-dct.cc
  ${LIB_SOURCE}/fallback-motion.cc 
  ${LIB_SOURCE}/fallback.cc
  ${LIB_SOURCE}/image-io.cc
  ${LIB_SOURCE}/image.cc
  ${LIB_SOURCE}/intrapred.cc
  ${LIB_SOURCE}/md5.cc
  ${LIB_SOURCE}/motion.cc
  ${LIB_SOURCE}/nal-parser.cc
  ${LIB_SOURCE}/nal.cc
  ${LIB_SOURCE}/pps.cc
  ${LIB_SOURCE}/quality.cc
  ${LIB_SOURCE}/refpic.cc
  ${LIB_SOURCE}/sao.cc
  ${LIB_SOURCE}/scan.cc
  ${LIB_SOURCE}/sei.cc
  ${LIB_SOURCE}/slice.cc
  ${LIB_SOURCE}/sps.cc
  ${LIB_SOURCE}/threads.cc
  ${LIB_SOURCE}/transform.cc
  ${LIB_SOURCE}/util.cc
  ${LIB_SOURCE}/visualize.cc
  ${LIB_SOURCE}/vps.cc
  ${LIB_SOURCE}/vui.cc
)

set(libde265_headers
  ${LIB_SOURCE}/acceleration.h
  ${LIB_SOURCE}/alloc_pool.h
  ${LIB_SOURCE}/bitstream.h
  ${LIB_SOURCE}/cabac.h
  ${LIB_SOURCE}/configparam.h
  ${LIB_SOURCE}/deblock.h
  ${LIB_SOURCE}/decctx.h
  ${LIB_SOURCE}/dpb.h
  ${LIB_SOURCE}/en265.h
  ${LIB_SOURCE}/fallback-dct.h
  ${LIB_SOURCE}/fallback-motion.h
  ${LIB_SOURCE}/fallback.h
  ${LIB_SOURCE}/image-io.h
  ${LIB_SOURCE}/image.h
  ${LIB_SOURCE}/intrapred.h
  ${LIB_SOURCE}/md5.h
  ${LIB_SOURCE}/motion.h
  ${LIB_SOURCE}/nal-parser.h
  ${LIB_SOURCE}/nal.h
  ${LIB_SOURCE}/pps.h
  ${LIB_SOURCE}/quality.h
  ${LIB_SOURCE}/refpic.h
  ${LIB_SOURCE}/sao.h
  ${LIB_SOURCE}/scan.h
  ${LIB_SOURCE}/sei.h
  ${LIB_SOURCE}/slice.h
  ${LIB_SOURCE}/sps.h
  ${LIB_SOURCE}/threads.h
  ${LIB_SOURCE}/transform.h
  ${LIB_SOURCE}/util.h
  ${LIB_SOURCE}/visualize.h
  ${LIB_SOURCE}/vps.h
  ${LIB_SOURCE}/vui.h
)

if(MSVC)
  set (libde265_sources
    ${libde265_sources}
    libde265/extra/win32cond.c
    libde265/extra/win32cond.h
  )
endif()

add_definitions(-DLIBDE265_EXPORTS)

add_subdirectory(${LIB_SOURCE}/encoder)

if(SUPPORTS_SSE4_1)
  add_definitions(-DHAVE_SSE4_1)
  add_subdirectory(${LIB_SOURCE}/x86)
endif()

add_library(${PROJECT_NAME} STATIC ${libde265_sources} ${ENCODER_OBJECTS} ${X86_OBJECTS})
target_link_libraries(${PROJECT_NAME} PRIVATE Threads::Threads)
target_compile_definitions(${PROJECT_NAME} PUBLIC LIBDE265_STATIC_BUILD)

write_basic_package_version_file(${PROJECT_NAME}ConfigVersion.cmake COMPATIBILITY ExactVersion)