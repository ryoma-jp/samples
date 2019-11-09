#! /bin/bash

input_file=./img/lena_gray.raw
output_dir=./result-runlength
output_file=${output_dir}/result.rle
flag=--enc
mkdir -p ${output_dir}
./comp_decomp ${flag} ${input_file} ${output_file}


