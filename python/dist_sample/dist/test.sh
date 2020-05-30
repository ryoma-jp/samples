#! /bin/bash

TEST_DIR='test'
LIB_DIR='build_lib'

mkdir -p $TEST_DIR
cd $TEST_DIR

cp ../../main.py .
cp ../$LIB_DIR/* .

python3 main.py

