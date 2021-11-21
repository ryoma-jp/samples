/**
 * @file rgb_deinterleave.c
 * @brief RGBインターリーブ画像データからRGBピクセル値を取得する
 */

#include <arm_neon.h>
#include "common.h"
#include "rgb_deinterleave.h"

/**
 * @brief RGBインターリーブ画像データからRGBピクセル値を取得する(C言語版)
 * @param src 入力RGBデータ
 * @param src_len 入力RGBデータのデータサイズ[byte]
 * @param dst RGBピクセル値を格納するバッファ(dst[R, G, B])
 * @return int 0固定
 * @details srcからRGBピクセル値を取得し，dstへ格納する
 */
int rgb_deinterleave_c(unsigned char* src, int src_len, unsigned char* dst[3])
{
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_c\n");
	
	unsigned char* r;
	unsigned char* g;
	unsigned char* b;
	int i;
	
	r = dst[0];
	g = dst[1];
	b = dst[2];

	for (i = 0; i < (src_len) / 3; i++) {
		r[i] = src[3*i];
		g[i] = src[3*i+1];
		b[i] = src[3*i+2];
	}
	
	return 0;
}

/**
 * @brief RGBインターリーブ画像データからRGBピクセル値を取得する(neon版)
 * @param src 入力RGBデータ
 * @param src_len 入力RGBデータのデータサイズ[byte]
 * @param dst RGBピクセル値を格納するバッファ(dst[R, G, B])
 * @return int 0固定
 * @details srcからRGBピクセル値を取得し，dstへ格納する
 */
int rgb_deinterleave_neon(unsigned char* src, int src_len, unsigned char* dst[3])
{
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_neon\n");

	unsigned char* r;
	unsigned char* g;
	unsigned char* b;
	uint8x16x3_t intlv_rgb;
	int num8x16 = src_len / 3 / 16;
	int i;
	
	r = dst[0];
	g = dst[1];
	b = dst[2];

	for (i=0; i < num8x16; i++) {
		intlv_rgb = vld3q_u8(src+3*16*i);
		vst1q_u8(r+16*i, intlv_rgb.val[0]);
		vst1q_u8(g+16*i, intlv_rgb.val[1]);
		vst1q_u8(b+16*i, intlv_rgb.val[2]);
	}
	
	
	return 0;
}

