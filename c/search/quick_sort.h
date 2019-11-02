
#ifndef __SORT_H__
#define __SORT_H__

#include <string.h>

/**
 * @enum _SORT_RET
 * @brief ソートプログラムの関数戻り値を定義
 */
typedef enum _SORT_RET {
	SORT_RET_NOERROR,	//! 正常終了
	SORT_RET_NULL,		//! NULL検出
} SORT_RET;

extern SORT_RET quick_sort(int* src, int key_num, int* dst);

#endif /*__SORT_H__ */
