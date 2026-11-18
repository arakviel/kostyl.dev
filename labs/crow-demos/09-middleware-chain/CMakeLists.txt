find_package(Crow CONFIG REQUIRED)

add_executable(middleware_chain src/main.cpp)
target_link_libraries(middleware_chain PRIVATE Crow::Crow)
