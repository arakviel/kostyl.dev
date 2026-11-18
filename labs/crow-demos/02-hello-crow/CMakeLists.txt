find_package(Crow CONFIG REQUIRED)

add_executable(hello_crow src/main.cpp)
target_link_libraries(hello_crow PRIVATE Crow::Crow)
