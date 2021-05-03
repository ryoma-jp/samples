#! /bin/bash

DEBUG="ON"		# ON or OFF

tflite_file='../tensorflow/output/tflite/converted_model.tflite'
#tflite_file='../tensorflow/output/tflite/converted_model-hidden_1.tflite'
input_file='../tensorflow/output/tflite/input_data.bin'
output_dir='./output'
output_csv="${output_dir}/output.csv"

mkdir -p ${output_dir}
if [ ${DEBUG} != "ON" ]; then
	./tflite_inference ${tflite_file} ${input_file} ${output_csv} 2>&1 | tee log.txt
else
	echo "run ${tflite_file} ${input_file} ${output_csv}"
	gdb ./tflite_inference
fi

