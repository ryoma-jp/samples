
#ifndef __SEARCH_H__
#define __SEARCH_H__

/**
 * @enum _SEARCH_RET
 * @brief 探索プログラムの関数戻り値を定義
 */
typedef enum _SEARCH_RET {
	SEARCH_RET_NOERROR,	//! 正常終了
	SEARCH_RET_NULL,	//! NULL検出
} SEARCH_RET;

extern int* linear_search(int* keys, int key_num, int search_key);
extern int* binary_search(int* keys, int key_num, int search_key);
extern int* hash_search(int* keys, int key_num, int search_key);

#endif /*__SEARCH_H__ */
