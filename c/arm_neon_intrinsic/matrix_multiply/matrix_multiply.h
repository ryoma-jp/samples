
#ifndef __MATRIX_MULTIPLY_H__
#define __MATRIX_MULTIPLY_H__

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <arm_neon.h>

extern int matrix_multiply_c(float32_t *A, float32_t *B, float32_t *C, uint32_t n, uint32_t m, uint32_t k);
extern int matrix_multiply_neon(float32_t  *A, float32_t  *B, float32_t *C, uint32_t n, uint32_t m, uint32_t k);
extern int matrix_multiply_4x4_neon(float32_t *A, float32_t *B, float32_t *C);
extern int print_matrix(float32_t *M, uint32_t cols, uint32_t rows);
extern int matrix_init_rand(float32_t *M, uint32_t numvals);
extern int matrix_init(float32_t *M, uint32_t cols, uint32_t rows, float32_t val);
extern bool matrix_comp(float32_t *A, float32_t *B, uint32_t rows, uint32_t cols);

#endif /*__MATRIX_MULTIPLY_H__ */
