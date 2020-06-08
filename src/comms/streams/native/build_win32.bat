@echo off
git submodule update --init --recursive
mkdir lib
mkdir build 
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Debug