find_package(Crow CONFIG REQUIRED)

add_executable(templates src/main.cpp)
target_link_libraries(templates PRIVATE Crow::Crow)

# Шлях до шаблонів зашито під час збірки, тому сервер можна запускати з будь-якої папки.
target_compile_definitions(templates PRIVATE
    TEMPLATES_DIR="${CMAKE_CURRENT_SOURCE_DIR}/templates")
