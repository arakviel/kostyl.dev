find_package(Crow CONFIG REQUIRED)

add_executable(middleware_practice src/main.cpp)
target_link_libraries(middleware_practice PRIVATE Crow::Crow)
