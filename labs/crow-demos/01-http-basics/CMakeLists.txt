cmake_minimum_required(VERSION 3.20)
project(http_basics LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(http_basics src/main.cpp)

if(WIN32)
    target_link_libraries(http_basics PRIVATE ws2_32)
endif()
