cmake_minimum_required(VERSION 3.16)
project(htw_cloud_protocol LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(htw_cloud_protocol STATIC
    src/error_code.cpp
)

target_include_directories(htw_cloud_protocol
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)
