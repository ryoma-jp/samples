#! /bin/bash

FILE_SIZE=100000000
OUTPUT_DIR="output"
OUTPUT_FILE="test_data.bin"

mkdir -p ${OUTPUT_DIR}
./generate_test_data ${FILE_SIZE} "${OUTPUT_DIR}/${OUTPUT_FILE}"

