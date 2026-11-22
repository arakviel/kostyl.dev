cmake_minimum_required(VERSION 3.20)
project(crud_todo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)

add_executable(crud_todo src/main.cpp)
target_link_libraries(crud_todo PRIVATE Crow::Crow)
