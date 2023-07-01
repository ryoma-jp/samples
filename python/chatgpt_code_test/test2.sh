#! /bin/bash

python3 test2/test2.py

gcc -o test2/test2 test2/test2.c
test2/test2

echo "diff test2/test2_result_python.txt test2/test2_result_c.txt"
diff test2/test2_result_python.txt test2/test2_result_c.txt
