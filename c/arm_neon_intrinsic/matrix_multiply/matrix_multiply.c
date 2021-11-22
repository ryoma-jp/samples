/**
 * @file matrix_multiply.c
 * @brief 行列計算
 */

#include "common.h"
#include "matrix_multiply.h"

/**
 * @brief 行列計算(C言語版)
 * @param A 入力行列(shape=[n, k])
 * @param B 入力行列(shape=[k, m])
 * @param C 出力行列(shape=[n, m])
 * @param n
 * @param m
 * @param k
 * @return int 0固定
 * @details 行列A[n, k]と行列B[k, m]の内積を計算し，C[n, m]を出力する
 */
int matrix_multiply_c(float32_t *A, float32_t *B, float32_t *C, uint32_t n, uint32_t m, uint32_t k) {
	for (int i_idx=0; i_idx<n; i_idx++) {
		for (int j_idx=0; j_idx<m; j_idx++) {
			C[n*j_idx + i_idx] = 0;
			for (int k_idx=0; k_idx<k; k_idx++) {
				C[n*j_idx + i_idx] += A[n*k_idx + i_idx]*B[k*j_idx + k_idx];
			}
		}
	}
	
	return 0;
}

/**
 * @brief 行列計算(Neon版)
 * @param A 入力行列(shape=[n, k])
 * @param B 入力行列(shape=[k, m])
 * @param C 出力行列(shape=[n, m])
 * @param n
 * @param m
 * @param k
 * @return int 0固定
 * @details 行列A[n, k]と行列B[k, m]の内積を計算し，C[n, m]を出力する
 */
int matrix_multiply_neon(float32_t  *A, float32_t  *B, float32_t *C, uint32_t n, uint32_t m, uint32_t k) {
	/* 
	 * Multiply matrices A and B, store the result in C. 
	 * It is the user's responsibility to make sure the matrices are compatible.
	 */     

	int A_idx;
	int B_idx;
	int C_idx;
	
	// these are the columns of a 4x4 sub matrix of A
	float32x4_t A0;
	float32x4_t A1;
	float32x4_t A2;
	float32x4_t A3;
	
	// these are the columns of a 4x4 sub matrix of B
	float32x4_t B0;
	float32x4_t B1;
	float32x4_t B2;
	float32x4_t B3;
	
	// these are the columns of a 4x4 sub matrix of C
	float32x4_t C0;
	float32x4_t C1;
	float32x4_t C2;
	float32x4_t C3;
	
	for (int i_idx=0; i_idx<n; i_idx+=4) {
		for (int j_idx=0; j_idx<m; j_idx+=4) {
			// Zero accumulators before matrix op
			C0 = vmovq_n_f32(0);
			C1 = vmovq_n_f32(0);
			C2 = vmovq_n_f32(0);
			C3 = vmovq_n_f32(0);
			for (int k_idx=0; k_idx<k; k_idx+=4) {
				// Compute base index to 4x4 block
				A_idx = i_idx + n*k_idx;
				B_idx = k*j_idx + k_idx;
				
				// Load most current A values in row 
				A0 = vld1q_f32(A+A_idx);
				A1 = vld1q_f32(A+A_idx+n);
				A2 = vld1q_f32(A+A_idx+2*n);
				A3 = vld1q_f32(A+A_idx+3*n);
				
				// Multiply accumulate in 4x1 blocks, i.e. each column in C
				B0 = vld1q_f32(B+B_idx);
				C0 = vfmaq_laneq_f32(C0, A0, B0, 0);
				C0 = vfmaq_laneq_f32(C0, A1, B0, 1);
				C0 = vfmaq_laneq_f32(C0, A2, B0, 2);
				C0 = vfmaq_laneq_f32(C0, A3, B0, 3);
				
				B1 = vld1q_f32(B+B_idx+k);
				C1 = vfmaq_laneq_f32(C1, A0, B1, 0);
				C1 = vfmaq_laneq_f32(C1, A1, B1, 1);
				C1 = vfmaq_laneq_f32(C1, A2, B1, 2);
				C1 = vfmaq_laneq_f32(C1, A3, B1, 3);
				
				B2 = vld1q_f32(B+B_idx+2*k);
				C2 = vfmaq_laneq_f32(C2, A0, B2, 0);
				C2 = vfmaq_laneq_f32(C2, A1, B2, 1);
				C2 = vfmaq_laneq_f32(C2, A2, B2, 2);
				C2 = vfmaq_laneq_f32(C2, A3, B2, 3);
				
				B3 = vld1q_f32(B+B_idx+3*k);
				C3 = vfmaq_laneq_f32(C3, A0, B3, 0);
				C3 = vfmaq_laneq_f32(C3, A1, B3, 1);
				C3 = vfmaq_laneq_f32(C3, A2, B3, 2);
				C3 = vfmaq_laneq_f32(C3, A3, B3, 3);
			}
			// Compute base index for stores
			C_idx = n*j_idx + i_idx;
			vst1q_f32(C+C_idx, C0);
			vst1q_f32(C+C_idx+n, C1);
			vst1q_f32(C+C_idx+2*n, C2);
			vst1q_f32(C+C_idx+3*n, C3);
		}
	}
	
	return 0;
}

/**
 * @brief 4x4行列計算(Neon版，ループアンローリング)
 * @param A 入力行列(shape=[4, 4])
 * @param B 入力行列(shape=[4, 4])
 * @param C 出力行列(shape=[4, 4])
 * @return int 0固定
 * @details 行列A[4, 4]と行列B[4, 4]の内積を計算し，C[4, 4]を出力する
 */
int matrix_multiply_4x4_neon(float32_t *A, float32_t *B, float32_t *C) {
	// these are the columns A
	float32x4_t A0;
	float32x4_t A1;
	float32x4_t A2;
	float32x4_t A3;
	
	// these are the columns B
	float32x4_t B0;
	float32x4_t B1;
	float32x4_t B2;
	float32x4_t B3;
	
	// these are the columns C
	float32x4_t C0;
	float32x4_t C1;
	float32x4_t C2;
	float32x4_t C3;
	
	A0 = vld1q_f32(A);
	A1 = vld1q_f32(A+4);
	A2 = vld1q_f32(A+8);
	A3 = vld1q_f32(A+12);
	
	// Zero accumulators for C values
	C0 = vmovq_n_f32(0);
	C1 = vmovq_n_f32(0);
	C2 = vmovq_n_f32(0);
	C3 = vmovq_n_f32(0);
	
	// Multiply accumulate in 4x1 blocks, i.e. each column in C
	B0 = vld1q_f32(B);
	C0 = vfmaq_laneq_f32(C0, A0, B0, 0);
	C0 = vfmaq_laneq_f32(C0, A1, B0, 1);
	C0 = vfmaq_laneq_f32(C0, A2, B0, 2);
	C0 = vfmaq_laneq_f32(C0, A3, B0, 3);
	vst1q_f32(C, C0);
	
	B1 = vld1q_f32(B+4);
	C1 = vfmaq_laneq_f32(C1, A0, B1, 0);
	C1 = vfmaq_laneq_f32(C1, A1, B1, 1);
	C1 = vfmaq_laneq_f32(C1, A2, B1, 2);
	C1 = vfmaq_laneq_f32(C1, A3, B1, 3);
	vst1q_f32(C+4, C1);
	
	B2 = vld1q_f32(B+8);
	C2 = vfmaq_laneq_f32(C2, A0, B2, 0);
	C2 = vfmaq_laneq_f32(C2, A1, B2, 1);
	C2 = vfmaq_laneq_f32(C2, A2, B2, 2);
	C2 = vfmaq_laneq_f32(C2, A3, B2, 3);
	vst1q_f32(C+8, C2);
	
	B3 = vld1q_f32(B+12);
	C3 = vfmaq_laneq_f32(C3, A0, B3, 0);
	C3 = vfmaq_laneq_f32(C3, A1, B3, 1);
	C3 = vfmaq_laneq_f32(C3, A2, B3, 2);
	C3 = vfmaq_laneq_f32(C3, A3, B3, 3);
	vst1q_f32(C+12, C3);
	
	return 0;
}

/**
 * @brief 行列を表示する
 * @param M 表示する行列
 * @param cols 列数
 * @param rows 行数
 * @return int 0固定
 * @details 行列M[cols, rows]を表示する
 */
int print_matrix(float32_t *M, uint32_t cols, uint32_t rows) {
	for (int i=0; i<rows; i++) {
		for (int j=0; j<cols; j++) {
			printf("%f ", M[j*rows + i]);
		}
		printf("\n");
	}
	printf("\n");
	
	return 0;
}

/**
 * @brief 行列を初期化する(乱数)
 * @param M 初期化する行列
 * @param numvals 行列内のデータの数(cols * rows)
 * @return int 0固定
 * @details 行列Mを初期化する
 */
int matrix_init_rand(float32_t *M, uint32_t numvals) {
	for (int i=0; i<numvals; i++) {
		M[i] = (float)rand()/(float)(RAND_MAX);
	}
	
	return 0;
}

/**
 * @brief 行列を初期化する(指定値)
 * @param M 初期化する行列
 * @param cols 列数
 * @param rows 行数
 * @param val 初期化する値
 * @return int 0固定
 * @details 行列M[cols, rows]を初期化値valで初期化する
 */
int matrix_init(float32_t *M, uint32_t cols, uint32_t rows, float32_t val) {
	for (int i=0; i<rows; i++) {
		for (int j=0; j<cols; j++) {
			M[j*rows + i] = val;
		}
	}
	
	return 0;
}

/**
 * @brief 2つの数値の不一致を判定する
 * @param a 比較する数値
 * @param b 比較する数値
 * @return bool 閾値未満でfalse，閾値以上でtrueを返す
 * @details 2つの数値の一致(閾値未満)でfalse，不一致(閾値以上)でtrueを返す
 */
bool f32comp_noteq(float32_t a, float32_t b) {
	if (fabs(a-b) < 0.000001) {
		return false;
	}
	return true;
}

/**
 * @brief 2つの行列の一致を判定する
 * @param A 比較する行列
 * @param B 比較する行列
 * @param rows 列数
 * @param cols 行数
 * @return bool 閾値以上でfalse，閾値未満でtrueを返す
 * @details 2つの行列の一致(閾値未満)でtrue，不一致(閾値未満)でfalseを返す
 */
bool matrix_comp(float32_t *A, float32_t *B, uint32_t rows, uint32_t cols) {
	float32_t a;
	float32_t b;
	for (int i=0; i<rows; i++) {
		for (int j=0; j<cols; j++) {
			a = A[rows*j + i];
			b = B[rows*j + i];
			
			if (f32comp_noteq(a, b)) {
				printf("i=%d, j=%d, A=%f, B=%f\n", i, j, a, b);
				return false;
			}
		}
	}
	return true;
}


