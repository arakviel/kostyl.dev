find_package(Crow CONFIG REQUIRED)

add_executable(json_crow src/main.cpp)
target_link_libraries(json_crow PRIVATE Crow::Crow)
