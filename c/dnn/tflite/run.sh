#! /bin/bash

tflite_file='../tensorflow/output/tflite/converted_model.tflite'
input_file='../tensorflow/output/tflite/input_data.bin'

./tflite_inference ${tflite_file} ${input_file} 2>&1 | tee log.txt


