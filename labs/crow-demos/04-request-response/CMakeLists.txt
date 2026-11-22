cmake_minimum_required(VERSION 3.20)
project(request_response LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)

add_executable(request_response src/main.cpp)
target_link_libraries(request_response PRIVATE Crow::Crow)
