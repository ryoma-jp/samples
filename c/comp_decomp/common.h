
#ifndef __COMMON_H__
#define __COMMON_H__

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/**
 * @def MY_PRINT_LVL_INFO
 * @brief 処理の進行情報などを表示する標準出力レベル
 */
#define MY_PRINT_LVL_INFO	(0x00000001)

/**
 * @def MY_PRINT_LVL_WARN
 * @brief 警告に相当する情報を表示する標準出力レベル
 */
#define MY_PRINT_LVL_WARN	(0x00000002)

/**
 * @def MY_PRINT_LVL_ERROR
 * @brief 処理エラーに相当する情報を表示する標準出力レベル
 */
#define MY_PRINT_LVL_ERROR	(0x00000004)	/**< 処理エラーに相当する情報 */

/**
 * @def MY_PRINT_LVL
 * @brief 標準出力する内容を定義
 * @details 標準出力レベルを"|"で繋いで標準出力する内容を設定する
 */
#define MY_PRINT_LVL		(MY_PRINT_LVL_INFO | MY_PRINT_LVL_WARN | MY_PRINT_LVL_ERROR)

/**
 * @def MY_PRINT
 * @brief 標準出力するプログラム共通の関数マクロ
 * @details MY_PRINT_LVLで定義された内容を標準出力する
 */
#define MY_PRINT(level, ...) { \
		if (level & MY_PRINT_LVL) { \
			struct timespec _ts; \
			clock_gettime(CLOCK_REALTIME, &_ts); \
			printf("[LVL:%08x][%6ld.%09ld] %s(L.%d) : ", level, _ts.tv_sec, _ts.tv_nsec, __func__, __LINE__); \
			printf(__VA_ARGS__); \
		} \
}

/**
 * @def MIN(a, b)
 * @brief 引数で指定されたa, bのうち小さい方を返す
 */
#ifndef  MIN
#define MIN(a, b)	(((a) < (b)) ? (a) : (b))
#endif
/**
 * @struct _GET_BITS_PARAM
 * @brief ビット取得処理用パラメータ
 */
typedef struct _GET_BITS_PARAM {
	char* src;		//!< データを読み出すバッファ
	unsigned int read_data;	//!< 取得データ
	unsigned int read_size;	//!< 取得データのサイズ(32bit以下をbit単位で指定)
	unsigned int byte_ptr;	//!< バイト単位のリードポインタ
	unsigned int bit_ptr;	//!< byte_ptr内のビット位置を示すリードポインタ
} GET_BITS_PARAM;

/**
 * @enum _GET_BITS_FLAG
 * @brief 2値データを表現するフラグ
 */
typedef enum _GET_BITS_FLAG {
	GET_BITS_FALSE=0,	//!< False
	GET_BITS_TRUE=1,	//!< True
} GET_BITS_FLAG;

/**
 * @struct _PUT_BITS_PARAM
 * @brief ビット書き込み処理用パラメータ
 */
typedef struct _PUT_BITS_PARAM {
	char* dst;		//!< 書き込み先のバッファ
	unsigned int put_data;	//!< 書き込むデータ
	int put_size;		//!< 書き込むデータのサイズ(32bit以下でbit単位で指定)
	unsigned int byte_ptr;	//!< バイト単位のリードポインタ
	unsigned int bit_ptr;	//!< byte_ptr内のビット位置を示すリードポインタ
} PUT_BITS_PARAM;

extern int get_bits(GET_BITS_PARAM *get_bits_param, GET_BITS_FLAG read_only);
extern int put_bits(PUT_BITS_PARAM* put_bits_param);

#endif /*__COMMON_H__ */
