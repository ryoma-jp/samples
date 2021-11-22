/**
 * @file main.c
 * @brief 行列計算のサンプル
 */

#include <time.h>
#include "common.h"
#include "matrix_multiply.h"

/** @def
 * Neon処理ブロックサイズ
 */
#define BLOCK_SIZE 4

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
int show_usage()
{
	printf("<< Usage >>\n");
	printf("  ./matrix_multiply\n");

	return 0;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details 行列計算のサンプル
 */
int main(int argc, char* argv[])
{
	/* --- 変数宣言 --- */
	uint32_t n = 2*BLOCK_SIZE; // rows in A
	uint32_t m = 2*BLOCK_SIZE; // cols in B
	uint32_t k = 2*BLOCK_SIZE; // cols in a and rows in b

	float32_t A[n*k];
	float32_t B[k*m];
	float32_t C[n*m];
	float32_t D[n*m];
	float32_t E[n*m];

	bool c_eq_neon;
	
	/* --- 引数処理 --- */
	if (argc != 1) {
		show_usage();
		return -1;
	}
	
	/* --- 行列の初期化(乱数で生成) --- */
	matrix_init_rand(A, n*k);
	matrix_init_rand(B, k*m);
	matrix_init(C, n, m, 0);

	print_matrix(A, k, n);
	print_matrix(B, m, k);
	//print_matrix(C, n, m);
	
	/* --- 行列計算 --- */
	matrix_multiply_c(A, B, E, n, m, k);
	printf("C\n");
	print_matrix(E, n, m);
	printf("===============================\n");

	matrix_multiply_neon(A, B, D, n, m, k);
	printf("Neon\n");
	print_matrix(D, n, m);
	c_eq_neon = matrix_comp(E, D, n, m);
	printf("Neon equal to C? %d\n", c_eq_neon);
	printf("===============================\n");
	
	return 0;
}

