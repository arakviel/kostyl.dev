cmake_minimum_required(VERSION 3.16)
project(Trainer CXX)
set(CMAKE_CXX_STANDARD 17)
add_executable(trainer main.cpp process_mac.cpp process_linux.cpp process_win.cpp)
