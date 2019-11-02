/**
 * @file search.c
 * @brief 探索プログラムのサンプル
 */

#include <search.h>
#include <common.h>

/**
 * @brief 線形探索
 * @param[in] keys 探索範囲
 * @param[in] key_num 探索範囲のサイズ(キー数)
 * @param[in] search_key 探索対象のキー
 * @return int* 探索対象キーが格納されているアドレス(=探索結果)
 *              探索対象キーが見つからない場合はNULLを返す
 * @details 線形探索を行う
 */
int* linear_search(int* keys, int key_num, int search_key)
{
	/* --- 変数宣言 --- */
	int* ret = NULL;
	int i;

	/* --- 探索 --- */
	for (i = 0; i < key_num; i++) {
		if (keys[i] == search_key) {
			ret = &keys[i];
			break;
		}
	}

	return ret;
}

/**
 * @brief 2分探索
 * @param[in] keys 探索範囲
 * @param[in] key_num 探索範囲のサイズ(キー数)
 * @param[in] search_key 探索対象のキー
 * @return int* 探索対象キーが格納されているアドレス(=探索結果)
 *              探索対象キーが見つからない場合はNULLを返す
 * @details 線形探索を行う
 */
int* binary_search(int* keys, int key_num, int search_key)
{
	/* --- 変数宣言 --- */
	int* ret;
	int low, high, middle;

	/* --- 初期値設定 --- */
	low = 0;
	high = key_num-1;
	middle = (low + high) / 2;

	/* --- 探索 --- */
	while ((low <= high) && (keys[middle] != search_key)) {
		if (keys[middle] > search_key) {
			high = middle - 1;
		} else {
			low = middle + 1;
		}
		middle = (low + high) / 2;
	}

	if (keys[middle] == search_key) {
		/* --- 探索成功 --- */
		ret = &keys[middle];
	} else {
		/* --- 探索失敗 --- */
		ret = NULL;
	}

	return ret;
}

/**
 * @brief ハッシュ探索
 * @param[in] keys 探索範囲
 * @param[in] key_num 探索範囲のサイズ(キー数)
 * @param[in] search_key 探索対象のキー
 * @return int* 探索対象キーが格納されているアドレス(=探索結果)
 *              探索対象キーが見つからない場合はNULLを返す
 * @details 線形探索を行う
 */
int* hash_search(int* keys, int key_num, int search_key)
{
	int* ret;

	return ret;
}

