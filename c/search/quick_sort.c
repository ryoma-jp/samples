/**
 * @file quick_sort.c
 * @brief クイックソート
 */

#include <quick_sort.h>
#include <common.h>

/**
 * @brief クイックソートのサブルーチン
 * @param[in,out] data ソート範囲 @n
 *                     ソート結果を上書き更新する
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @return SORT_RET
 * @details クイックソートによるソート処理のサブルーチン @n
 *          再帰的処理による分割処理
 */
static SORT_RET quick_sort_sub(int* data, int key_num)
{
	SORT_RET ret = SORT_RET_NOERROR;
	int pivot = data[key_num-1];
	int left_ptr = 0;
	int right_ptr = key_num-1;
	int data_tmp;

	while (left_ptr < right_ptr) {
		while ((data[left_ptr] < pivot)) {
			left_ptr += 1;
		}
		while ((pivot <= data[right_ptr]) && (left_ptr < right_ptr)) {
			right_ptr -= 1;
		}

		if (left_ptr < right_ptr) {
			data_tmp = data[left_ptr];
			data[left_ptr] = data[right_ptr];
			data[right_ptr] = data_tmp;
		}
	}
	data[key_num-1] = data[left_ptr];
	data[left_ptr] = pivot;

	if (left_ptr > 1) {
		quick_sort_sub(data, left_ptr);
	}
	if (key_num - (right_ptr+1) > 1) {
		quick_sort_sub(&data[right_ptr+1], key_num - (right_ptr+1));
	}

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

	quick_sort_sub(dst, key_num);

	return ret;
}


