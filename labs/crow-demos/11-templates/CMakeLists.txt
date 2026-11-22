cmake_minimum_required(VERSION 3.20)
project(templates LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)

add_executable(templates src/main.cpp)
target_link_libraries(templates PRIVATE Crow::Crow)

# Шлях до шаблонів зашито під час збірки, тому сервер можна запускати з будь-якої папки.
target_compile_definitions(templates PRIVATE
    TEMPLATES_DIR="${CMAKE_CURRENT_SOURCE_DIR}/templates")
