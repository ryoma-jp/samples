#! /bin/bash

python3 test3/test3.py

gcc -o test3/test3 test3/test3.c
test3/test3

echo "diff test3/test3_result_python.txt test3/test3_result_c.txt"
diff test3/test3_result_python.txt test3/test3_result_c.txt
