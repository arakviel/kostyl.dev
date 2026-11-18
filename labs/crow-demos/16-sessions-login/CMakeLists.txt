find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(unofficial-argon2 CONFIG REQUIRED)

add_executable(sessions_login src/main.cpp)
target_include_directories(sessions_login PRIVATE include)
target_link_libraries(sessions_login PRIVATE
    Crow::Crow nlohmann_json::nlohmann_json unofficial::argon2::libargon2)
