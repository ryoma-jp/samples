#! /bin/bash

python main.py --command exit --pid $1
ps -aux

python main.py --list

