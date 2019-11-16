#! /bin/bash

input_file=./img/lena_gray.raw
output_dir=./result-runlength
output_file=${output_dir}/result-8_8.rle
flag=--enc
enc_unit=8
enc_len_unit=8
mkdir -p ${output_dir}
./comp_decomp ${flag} ${input_file} ${output_file} ${enc_unit} ${enc_len_unit}

input_file=./img/lena_gray.raw
output_dir=./result-runlength
output_file=${output_dir}/result-1_7.rle
flag=--enc
enc_unit=1
enc_len_unit=7
mkdir -p ${output_dir}
./comp_decomp ${flag} ${input_file} ${output_file} ${enc_unit} ${enc_len_unit}


