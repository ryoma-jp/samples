
#ifndef __COMMON_H__
#define __COMMON_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/**
 * @def DNN_PRINT_LVL_INFO
 * @brief 処理の進行情報などを表示する標準出力レベル
 */
#define DNN_PRINT_LVL_INFO	(0x00000001)

/**
 * @def DNN_PRINT_LVL_WARN
 * @brief 警告に相当する情報を表示する標準出力レベル
 */
#define DNN_PRINT_LVL_WARN	(0x00000002)

/**
 * @def DNN_PRINT_LVL_ERROR
 * @brief 処理エラーに相当する情報を表示する標準出力レベル
 */
#define DNN_PRINT_LVL_ERROR	(0x00000004)	/**< 処理エラーに相当する情報 */

/**
 * @def DNN_PRINT_LVL
 * @brief 標準出力する内容を定義
 * @details 標準出力レベルを"|"で繋いで標準出力する内容を設定する
 */
#define DNN_PRINT_LVL		(DNN_PRINT_LVL_INFO | DNN_PRINT_LVL_WARN | DNN_PRINT_LVL_ERROR)

/**
 * @def DNN_PRINT
 * @brief 標準出力するプログラム共通の関数マクロ
 * @details DNN_PRINT_LVLで定義された内容を標準出力する
 */
#define DNN_PRINT(level, ...) { \
		if (level & DNN_PRINT_LVL) { \
			struct timespec _ts; \
			clock_gettime(CLOCK_REALTIME, &_ts); \
			printf("[LVL:%08x][%6ld.%09ld] %s(L.%d) : ", level, _ts.tv_sec, _ts.tv_nsec, __func__, __LINE__); \
			printf(__VA_ARGS__); \
		} \
}

#endif /*__COMMON_H__ */
