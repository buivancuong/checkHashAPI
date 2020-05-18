cmake_minimum_required(VERSION 3.16)
project(bf_httpserver)

set(CMAKE_CXX_STANDARD 14)

add_executable(bf_server bf_server.cpp)
add_executable(bf_client bf_client.cpp)
