cmake_minimum_required(VERSION 3.20)
project(CrowDemos LANGUAGES CXX)

enable_testing()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(MSVC)
    add_compile_options(/W4 /utf-8)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Кожна підпапка — демо однієї лекції. Прикріплюється, якщо папка існує.
file(GLOB DEMO_DIRS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} CONFIGURE_DEPENDS "[0-9][0-9]-*")
list(SORT DEMO_DIRS)
foreach(dir IN LISTS DEMO_DIRS)
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${dir}/CMakeLists.txt)
        add_subdirectory(${dir})
    endif()
endforeach()
