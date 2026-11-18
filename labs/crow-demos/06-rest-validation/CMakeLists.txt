find_package(Crow CONFIG REQUIRED)

add_executable(rest_validation src/main.cpp)
target_link_libraries(rest_validation PRIVATE Crow::Crow)
