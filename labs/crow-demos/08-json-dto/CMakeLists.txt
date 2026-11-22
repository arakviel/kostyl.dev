cmake_minimum_required(VERSION 3.20)
project(json_dto LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

add_executable(json_dto src/main.cpp)
target_link_libraries(json_dto PRIVATE Crow::Crow nlohmann_json::nlohmann_json)
