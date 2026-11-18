find_package(Crow CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

# Чотири етапи еволюції доступу до даних. Усі віддають однаковий API:
#   GET /users, POST /users, GET /users/<id>
foreach(stage IN ITEMS stage1_direct stage2_functions stage3_dao stage4_active_record)
    add_executable(dal_${stage} src/${stage}.cpp)
    target_link_libraries(dal_${stage} PRIVATE Crow::Crow nlohmann_json::nlohmann_json)
    target_include_directories(dal_${stage} PRIVATE src)
endforeach()
