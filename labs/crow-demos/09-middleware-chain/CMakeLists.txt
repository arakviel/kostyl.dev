cmake_minimum_required(VERSION 3.20)
project(middleware_chain LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)

add_executable(middleware_chain src/main.cpp)
target_link_libraries(middleware_chain PRIVATE Crow::Crow)
