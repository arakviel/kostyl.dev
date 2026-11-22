cmake_minimum_required(VERSION 3.20)
project(json_crow LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)

add_executable(json_crow src/main.cpp)
target_link_libraries(json_crow PRIVATE Crow::Crow)
