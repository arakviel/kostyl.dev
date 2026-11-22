cmake_minimum_required(VERSION 3.20)
project(rbac_security LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(unofficial-argon2 CONFIG REQUIRED)

add_executable(rbac_security src/main.cpp)
target_include_directories(rbac_security PRIVATE include)
target_link_libraries(rbac_security PRIVATE
    Crow::Crow nlohmann_json::nlohmann_json unofficial::argon2::libargon2)
