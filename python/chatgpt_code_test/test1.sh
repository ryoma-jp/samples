#! /bin/bash

gcc -o test1/test1 test1/test1.c
test1/test1

echo "diff test1/test1_exp.txt test1/test1_result_c.txt"

# test1/test1_exp.txt is an expectation
diff test1/test1_exp.txt test1/test1_result_c.txt
