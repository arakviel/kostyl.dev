add_executable(http_basics src/main.cpp)

if(WIN32)
    target_link_libraries(http_basics PRIVATE ws2_32)
endif()
