find_package(Crow CONFIG REQUIRED)

add_executable(crud_todo src/main.cpp)
target_link_libraries(crud_todo PRIVATE Crow::Crow)
