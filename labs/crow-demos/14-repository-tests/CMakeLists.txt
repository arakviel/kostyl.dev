find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(doctest CONFIG REQUIRED)

# Ядро: домен, інтерфейс репозиторію, реалізації, HTTP-шар. Лише заголовки.
add_library(repo_core INTERFACE)
target_include_directories(repo_core INTERFACE include)
target_link_libraries(repo_core INTERFACE Crow::Crow nlohmann_json::nlohmann_json)

add_executable(repository_api src/main.cpp)
target_link_libraries(repository_api PRIVATE repo_core)

add_executable(repository_unit_tests
    tests/test_main.cpp
    tests/test_user_service.cpp
    tests/test_repository_contract.cpp)
target_link_libraries(repository_unit_tests PRIVATE repo_core doctest::doctest)

add_test(NAME repository_unit_tests COMMAND repository_unit_tests)
