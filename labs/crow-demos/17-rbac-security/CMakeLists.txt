find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(unofficial-argon2 CONFIG REQUIRED)

add_executable(rbac_security src/main.cpp)
target_include_directories(rbac_security PRIVATE include)
target_link_libraries(rbac_security PRIVATE
    Crow::Crow nlohmann_json::nlohmann_json unofficial::argon2::libargon2)
