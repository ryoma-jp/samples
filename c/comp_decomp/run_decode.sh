#! /bin/bash

input_file=./result-runlength/result-8_8.rle
output_dir=./result-runlength
output_file=${output_dir}/result-8_8.bin
flag=--rl_dec
mkdir -p ${output_dir}
./comp_decomp ${flag} ${input_file} ${output_file} 

input_file=./result-runlength/result-1_7.rle
output_dir=./result-runlength
output_file=${output_dir}/result-1_7.bin
flag=--rl_dec
mkdir -p ${output_dir}
./comp_decomp ${flag} ${input_file} ${output_file}


