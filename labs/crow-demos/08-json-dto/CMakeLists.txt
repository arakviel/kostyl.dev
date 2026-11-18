find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

add_executable(json_dto src/main.cpp)
target_link_libraries(json_dto PRIVATE Crow::Crow nlohmann_json::nlohmann_json)
