
#ifndef __SEARCH_H__
#define __SEARCH_H__

#include <stdio.h>

/**
 * @enum _SEARCH_RET
 * @brief 探索プログラムの関数戻り値を定義
 */
typedef enum _SEARCH_RET {
	SEARCH_RET_NOERROR,			//! 正常終了
	SEARCH_RET_NULL,			//! NULL検出
	SEARCH_RET_HASH_TABLE_CREATE_FAILED,	//! ハッシュテーブル生成失敗
} SEARCH_RET;

/**
 * @enum _HASH_SEARCH_TYPE
 * @brief ハッシュ探索方法
 */
typedef enum _HASH_SEARCH_TYPE {
	HASH_SEARCH_TYPE_OPEN_ADDRESS, //! オープンアドレス法
	HASH_SEARCH_TYPE_CHAIN, //! チェイン法
} HASH_SEARCH_TYPE;

/**
 * @enum _HASH_TABLE_STATE
 * @brief ハッシュテーブルの空き状態
 */
typedef enum _HASH_TABLE_STATE {
	HASH_TABLE_STATE_EMPTY = 0,	//! 空き
	HASH_TABLE_STATE_FULL,		//! データ格納済み
} HASH_TABLE_STATE;

/**
 * @struct _HASH_TABLE_CHAIN
 * @brief ハッシュテーブルのリスト
 */
typedef struct _HASH_TABLE {
	int key;			//! 格納するデータ
	HASH_TABLE_STATE state;		//! データの空き状態
	struct _HASH_TABLE* next;	//! シノニムを格納する次のアドレス(チェイン法でのみ使用する)
} HASH_TABLE;

/**
 * @def HASH_TABLE_SIZE_OPEN_ADDRESS
 * @brief ハッシュテーブルのサイズ(オープンアドレス法, 40KB暫定)
 */
#define HASH_TABLE_SIZE_OPEN_ADDRESS	(40960)

/**
 * @def HASH_TABLE_SIZE_CHAIN
 * @brief ハッシュテーブルのサイズ(オープンアドレス法, 1KB暫定)
 */
#define HASH_TABLE_SIZE_CHAIN	(1024)


extern int* linear_search(int* keys, int key_num, int search_key);
extern int* binary_search(int* keys, int key_num, int search_key);
extern int* hash_search(HASH_TABLE* hash_table, int search_key, HASH_SEARCH_TYPE search_type);
extern SEARCH_RET hash_table_create(int* keys, int key_num, HASH_SEARCH_TYPE search_type, HASH_TABLE* hash_table);
extern SEARCH_RET hash_table_save(FILE* fp_save, HASH_TABLE* hash_table, HASH_SEARCH_TYPE search_type);

#endif /*__SEARCH_H__ */
