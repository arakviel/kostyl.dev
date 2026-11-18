find_package(Crow CONFIG REQUIRED)

add_executable(request_response src/main.cpp)
target_link_libraries(request_response PRIVATE Crow::Crow)
