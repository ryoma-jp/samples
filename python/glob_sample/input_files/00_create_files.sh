#! /bin/bash

CREATE_FILE_NUM=1000

for i in `seq ${CREATE_FILE_NUM}`
do
	touch "sample_file_${i}.bin"
done

mkdir -p sub_dir
cd sub_dir

for i in `seq ${CREATE_FILE_NUM}`
do
	touch "sample_file_${i}.bin"
done

cd ..
