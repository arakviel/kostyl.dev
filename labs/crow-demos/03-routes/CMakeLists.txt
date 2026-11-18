find_package(Crow CONFIG REQUIRED)

add_executable(routes src/main.cpp)
target_link_libraries(routes PRIVATE Crow::Crow)
