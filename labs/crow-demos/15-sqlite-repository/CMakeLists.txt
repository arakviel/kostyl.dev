cmake_minimum_required(VERSION 3.20)
project(sqlite_repository LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(doctest CONFIG REQUIRED)
find_package(unofficial-sqlite3 CONFIG REQUIRED)

# Домен, інтерфейс і HTTP-шар — копія з демо 14 (папка самодостатня).
# Нове тут: infra/sqlite_user_repository.hpp.
add_library(sqlite_repo_core INTERFACE)
target_include_directories(sqlite_repo_core INTERFACE include)
target_link_libraries(sqlite_repo_core INTERFACE
    Crow::Crow nlohmann_json::nlohmann_json unofficial::sqlite3::sqlite3)

add_executable(sqlite_repository_api src/main.cpp)
target_link_libraries(sqlite_repository_api PRIVATE sqlite_repo_core)

add_executable(sqlite_repository_tests
    tests/test_main.cpp
    tests/test_contract.cpp
    tests/test_sqlite.cpp)
target_link_libraries(sqlite_repository_tests PRIVATE sqlite_repo_core doctest::doctest)

enable_testing()
add_test(NAME sqlite_repository_tests COMMAND sqlite_repository_tests)
