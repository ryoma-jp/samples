/**
 * @file sort.c
 * @brief ソートプログラムのサンプル
 */

#include <sort.h>
#include <common.h>

/**
 * @brief 選択法
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return SORT_RET
 * @details 選択法によるソート処理
 */
SORT_RET selection_sort(int* src, int key_num, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;
	int sorted_ptr = 0;
	int search_ptr = sorted_ptr;
	int min_ptr;
	int data_tmp;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	for (sorted_ptr = 0; sorted_ptr < key_num-1; sorted_ptr++) {
		min_ptr = sorted_ptr;
		for (search_ptr = sorted_ptr+1; search_ptr < key_num; search_ptr++) {
			min_ptr = (dst[search_ptr] < dst[min_ptr]) ? search_ptr : min_ptr;
		}
		data_tmp = dst[sorted_ptr];
		dst[sorted_ptr] = dst[min_ptr];
		dst[min_ptr] = data_tmp;
	}

	return ret;
}

/**
 * @brief バブルソート
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return SORT_RET
 * @details バブルソートによるソート処理
 */
SORT_RET bubble_sort(int* src, int key_num, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;
	int iter = 0;
	int sorted_ptr = 0;
	int data_tmp;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	for (iter = 0; iter < key_num-1; iter++) {
		for (sorted_ptr = 0; sorted_ptr < key_num-1-iter; sorted_ptr++) {
			if (dst[sorted_ptr+1] < dst[sorted_ptr]) {
				data_tmp = dst[sorted_ptr];
				dst[sorted_ptr] = dst[sorted_ptr+1];
				dst[sorted_ptr+1] = data_tmp;
			}
		}
	}

	return ret;
}

/**
 * @brief 挿入法サブルーチン
 * @param[in,out] data ソート範囲 @n
 *                 ソート結果は上書きする
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[in] h ソート間隔
 * @return SORT_RET
 * @details 挿入法／シェルソート用のサブルーチン
 */
static SORT_RET insert_sort_sub(int* data, int key_num, int h)
{
	SORT_RET ret = SORT_RET_NOERROR;
	int sorted_ptr = 0;
	int insert_ptr = 0;
	int data_tmp;

	for (sorted_ptr = h; sorted_ptr < key_num*h; sorted_ptr+=h) {
		data_tmp = data[sorted_ptr];
		insert_ptr = sorted_ptr;
		while ((data_tmp < data[insert_ptr-h]) && (insert_ptr > 0)) {
			data[insert_ptr] = data[insert_ptr-h];
			insert_ptr -= h;
		}
		data[insert_ptr] = data_tmp;
	}
	
	return ret;
}

/**
 * @brief 挿入法
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return SORT_RET
 * @details 挿入法によるソート処理
 */
SORT_RET insert_sort(int* src, int key_num, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	insert_sort_sub(dst, key_num, 1);

	return ret;
}

/**
 * @brief シェルソート
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return SORT_RET
 * @details シェルソートによるソート処理
 */
SORT_RET shell_sort(int* src, int key_num, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;
	int h_coef = 10;
	int h;
	int iter;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	do {
		h = (1 > key_num / h_coef) ? 1 : (key_num / h_coef);
		for (iter = 0; iter < h; iter++) {
			insert_sort_sub(&dst[iter], h_coef, h);
		}
		h_coef *= 10;
	} while (h > 1);

	return ret;
}

/**
 * @brief クイックソート
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return SORT_RET
 * @details クイックソートによるソート処理
 */
SORT_RET quick_sort(int* src, int key_num, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	return ret;
}

/**
 * @brief ヒープソート
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return SORT_RET
 * @details ヒープソートによるソート処理
 */
SORT_RET heap_sort(int* src, int key_num, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	return ret;
}

/**
 * @brief マージソート
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return SORT_RET
 * @details マージソートによるソート処理
 */
SORT_RET merge_sort(int* src, int key_num, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	return ret;
}

