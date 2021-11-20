
cmake_minimum_required(VERSION 3.16)
project(inference_sample C CXX)

set(TENSORFLOW_SOURCE_DIR "" CACHE PATH
  "Directory that contains the TensorFlow project"
)
message("TENSORFLOW_SOURCE_DIR: ${TENSORFLOW_SOURCE_DIR}")

if(NOT TENSORFLOW_SOURCE_DIR)
  get_filename_component(TENSORFLOW_SOURCE_DIR
    "../tensorflow_src"
    ABSOLUTE
  )
endif()

add_subdirectory(
  "${TENSORFLOW_SOURCE_DIR}/tensorflow/lite"
  "../tflite_build/"
  EXCLUDE_FROM_ALL
)

set(CMAKE_CXX_STANDARD 11)
add_executable(inference_sample
  main.cpp
)
target_link_libraries(inference_sample
  tensorflow-lite
)
