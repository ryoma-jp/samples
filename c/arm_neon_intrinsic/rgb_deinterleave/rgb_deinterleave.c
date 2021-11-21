/**
 * @file rgb_deinterleave.c
 * @brief RGBインターリーブ画像データからRGBピクセル値を取得する
 */

#include "common.h"
#include "rgb_deinterleave.h"

/**
 * @brief RGBインターリーブ画像データからRGBピクセル値を取得する(C言語版)
 * @param src 入力RGBデータ
 * @param dst RGBピクセル値を格納するバッファ(dst[R, G, B])
 * @return int 0固定
 * @details srcからRGBピクセル値を取得し，dstへ格納する
 */
int rgb_deinterleave_c(char* src, char* dst[3])
{
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_c\n");

	return 0;
}

/**
 * @brief RGBインターリーブ画像データからRGBピクセル値を取得する(neon版)
 * @param src 入力RGBデータ
 * @param dst RGBピクセル値を格納するバッファ(dst[R, G, B])
 * @return int 0固定
 * @details srcからRGBピクセル値を取得し，dstへ格納する
 */
int rgb_deinterleave_neon(char* src, char* dst[3])
{
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_neon\n");

	return 0;
}

