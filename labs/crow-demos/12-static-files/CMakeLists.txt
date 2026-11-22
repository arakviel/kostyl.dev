cmake_minimum_required(VERSION 3.20)
project(static_files LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)

add_executable(static_files src/main.cpp)
target_link_libraries(static_files PRIVATE Crow::Crow)

# CROW_STATIC_DIRECTORY задає папку для вбудованого маршруту /static/<path> (кінцевий слеш обов'язковий).
target_compile_definitions(static_files PRIVATE
    CROW_STATIC_DIRECTORY="${CMAKE_CURRENT_SOURCE_DIR}/static/"
    DOWNLOADS_DIR="${CMAKE_CURRENT_SOURCE_DIR}/downloads")
