/**
 * @file search.c
 * @brief 探索プログラムのサンプル
 */

#include <string.h>
#include "search.h"
#include "common.h"

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
 * @brief ハッシュテーブル生成(オープンアドレス法)
 * @param[in] keys 探索範囲
 * @param[in] key_num 探索範囲のサイズ(キー数)
 * @param[out] hash_table ハッシュテーブル
 * @param[out] hash_table_state ハッシュテーブルの空き状態 @n
 *             (HASH_TABLE_STATE_FULL : データ格納済み，HASH_TABLE_STATE_EMPTY : 空き)
 * @return SEARCH_RET
 * @details ハッシュテーブルを生成する(オープンアドレス法)
 */
static SEARCH_RET hash_table_create_open_address(
		int* keys, int key_num, HASH_TABLE* hash_table)
{
	SEARCH_RET ret = SEARCH_RET_NOERROR;
	int iter;
	int hash_idx;
	int synonym_cnt;

	memset(hash_table, 0, HASH_TABLE_SIZE_OPEN_ADDRESS * sizeof(HASH_TABLE));
	for (iter = 0; iter < key_num; iter++) {
		hash_idx = keys[iter] % key_num;
		synonym_cnt = 0;

		while (synonym_cnt < HASH_TABLE_SIZE_OPEN_ADDRESS) {
			if (hash_table[hash_idx].state == HASH_TABLE_STATE_EMPTY) {
				hash_table[hash_idx].key = keys[iter];
				hash_table[hash_idx].state = HASH_TABLE_STATE_FULL;
				break;
			} else {
				synonym_cnt += 1;
				hash_idx = (keys[iter] + synonym_cnt) % key_num;
			}
		}
		if (synonym_cnt >= HASH_TABLE_SIZE_OPEN_ADDRESS) {
			ret = SEARCH_RET_HASH_TABLE_CREATE_FAILED;
			break;
		}
	}

	return ret;
}

/**
 * @brief ハッシュテーブル生成(チェイン法)
 * @param[in] keys 探索範囲
 * @param[in] key_num 探索範囲のサイズ(キー数)
 * @param[out] hash_table ハッシュテーブル
 * @return SEARCH_RET
 * @details ハッシュテーブルを生成する(オープンアドレス法)
 */
static SEARCH_RET hash_table_create_chain(
		int* keys, int key_num, HASH_TABLE* hash_table) 
{
	SEARCH_RET ret = SEARCH_RET_NOERROR;
	HASH_TABLE* hash_table_work;
	int iter;
	int hash_idx;

	memset(hash_table, 0, HASH_TABLE_SIZE_CHAIN * sizeof(HASH_TABLE));
	for (iter = 0; iter < key_num; iter++) {
		hash_idx = keys[iter] % HASH_TABLE_SIZE_CHAIN;

		if (hash_table[hash_idx].state == HASH_TABLE_STATE_EMPTY) {
			hash_table[hash_idx].key = keys[iter];
			hash_table[hash_idx].state = HASH_TABLE_STATE_FULL;
		} else {
			if (hash_table[hash_idx].next == NULL) {
				hash_table[hash_idx].next = (HASH_TABLE*)malloc(sizeof(HASH_TABLE));
				hash_table_work = hash_table[hash_idx].next;
			} else {
				hash_table_work = hash_table[hash_idx].next;
				while (hash_table_work->next != NULL) {
					hash_table_work = hash_table_work->next;
				}
				hash_table_work->next = (HASH_TABLE*)malloc(sizeof(HASH_TABLE));
				hash_table_work = hash_table_work->next;
			}
			hash_table_work->key = keys[iter];
			hash_table_work->state = HASH_TABLE_STATE_FULL;
			hash_table_work->next = NULL;
		}
	}

	return ret;
}

/**
 * @brief ハッシュテーブル生成
 * @param[in] keys 探索範囲
 * @param[in] key_num 探索範囲のサイズ(キー数)
 * @param[in] search_type ハッシュ探索方法
 * @param[out] hash_table 生成したハッシュテーブル
 * @return SEARCH_RET
 * @details ハッシュテーブル生成を行う
 */
SEARCH_RET hash_table_create(int* keys, int key_num, HASH_SEARCH_TYPE search_type, HASH_TABLE* hash_table)
{
	SEARCH_RET ret = SEARCH_RET_NOERROR;

	switch (search_type) {
		case HASH_SEARCH_TYPE_OPEN_ADDRESS:
			ret = hash_table_create_open_address(keys, key_num, hash_table);
			break;
		case HASH_SEARCH_TYPE_CHAIN:
			ret = hash_table_create_chain(keys, key_num, hash_table);
			break;
		default:
			MY_PRINT(MY_PRINT_LVL_ERROR, "Unknown search_type\n");
			exit(0);
	}

	return ret;
}

/**
 * @brief ハッシュテーブル保存
 * @param[in] fp_save 保存先のファイルポインタ
 * @param[in] hash_table 保存するハッシュテーブル
 * @param[in] search_type ハッシュ探索方法(テーブルサイズ判断用)
 * @return SEARCH_RET
 * @details ハッシュテーブル生成を行う
 */
SEARCH_RET hash_table_save(FILE* fp_save, HASH_TABLE* hash_table, HASH_SEARCH_TYPE search_type)
{
	SEARCH_RET ret = SEARCH_RET_NOERROR;
	HASH_TABLE* hash_table_work;
	int hash_table_size;
	int iter;

	hash_table_size = (search_type == HASH_SEARCH_TYPE_OPEN_ADDRESS) ? 
		HASH_TABLE_SIZE_OPEN_ADDRESS : HASH_TABLE_SIZE_CHAIN;

	fprintf(fp_save, "addr,value\n");
	for (iter = 0; iter < hash_table_size; iter++) {
		hash_table_work = &hash_table[iter];
		while (hash_table_work != NULL) {
			if (hash_table_work->state == HASH_TABLE_STATE_FULL) {
				fprintf(fp_save, "%p,%d\n", &(hash_table_work->key), hash_table_work->key);
			} else {
				fprintf(fp_save, "%p,empty\n", hash_table_work);
			}
			hash_table_work = hash_table_work->next;
		}
	}

	return ret;
}

/**
 * @brief ハッシュ探索(オープンアドレス法)
 * @param[in] hash_table 探索範囲(hash_table_createで生成したテーブルを指定)
 * @param[in] search_key 探索対象のキー
 * @return int* 探索対象キーが格納されているアドレス(=探索結果)
 *              探索対象キーが見つからない場合はNULLを返す
 * @details ハッシュ探索(オープンアドレス法)を行う
 */
int* hash_search_open_address(HASH_TABLE* hash_table, int search_key)
{
	int* ret = NULL;
	int hash_key;
	int key_found = 0;
	int retry_cnt = 0;

	while (key_found == 0) {
		hash_key = ((search_key + retry_cnt) % HASH_TABLE_SIZE_OPEN_ADDRESS);
		if (hash_table[hash_key].state == HASH_TABLE_STATE_EMPTY) {
			break;
		} else {
			if (hash_table[hash_key].key == search_key) {
				ret = &(hash_table[hash_key].key);
				key_found = 1;
			} else {
				retry_cnt += 1;
				if (retry_cnt >= HASH_TABLE_SIZE_OPEN_ADDRESS) {
					break;
				}
			}
		}
	}

	return ret;
}

/**
 * @brief ハッシュ探索(チェイン法)
 * @param[in] hash_table 探索範囲(hash_table_createで生成したテーブルを指定)
 * @param[in] search_key 探索対象のキー
 * @return int* 探索対象キーが格納されているアドレス(=探索結果)
 *              探索対象キーが見つからない場合はNULLを返す
 * @details ハッシュ探索(チェイン法)を行う
 */
int* hash_search_chain(HASH_TABLE* hash_table, int search_key)
{
	int* ret = NULL;
	HASH_TABLE* hash_table_work;
	int hash_key;
	int key_found = 0;

	while (key_found == 0) {
		hash_key = search_key % HASH_TABLE_SIZE_CHAIN;
		if (hash_table[hash_key].state == HASH_TABLE_STATE_EMPTY) {
			break;
		} else {
			if (hash_table[hash_key].key == search_key) {
				ret = &(hash_table[hash_key].key);
				key_found = 1;
			} else {
				hash_table_work = hash_table[hash_key].next;
				while ((hash_table_work != NULL) && (hash_table_work->key != search_key)) {
					hash_table_work = hash_table_work->next;
				}
				if (hash_table_work != NULL) {
					ret = &(hash_table_work->key);
					key_found = 1;
				} else {
					break;
				}
			}
		}
	}

	return ret;
}

/**
 * @brief ハッシュ探索
 * @param[in] hash_table 探索範囲(hash_table_createで生成したテーブルを指定)
 * @param[in] search_key 探索対象のキー
 * @param[in] search_type ハッシュ探索の方法
 * @return int* 探索対象キーが格納されているアドレス(=探索結果)
 *              探索対象キーが見つからない場合はNULLを返す
 * @details ハッシュ探索を行う
 */
int* hash_search(HASH_TABLE* hash_table, int search_key, HASH_SEARCH_TYPE search_type)
{
	int* ret = NULL;

	switch (search_type) {
		case HASH_SEARCH_TYPE_OPEN_ADDRESS:
			ret = hash_search_open_address(hash_table, search_key);
			break;
		case HASH_SEARCH_TYPE_CHAIN:
			ret = hash_search_chain(hash_table, search_key);
			break;
		default:
			break;
	}

	return ret;
}

