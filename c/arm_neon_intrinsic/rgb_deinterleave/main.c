/**
 * @file main.c
 * @brief RGBインターリーブ画像データからRGBピクセル値を取得する
 */

#include <time.h>
#include "common.h"
#include "rgb_deinterleave.h"

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
int show_usage()
{
	printf("<< Usage >>\n");
	printf("  ./rgb_deinterleave\n");

	return 0;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details RGBインターリーブ画像データからRGBピクセル値を取得する処理時間を計測する
 */
int main(int argc, char* argv[])
{
	/* --- 変数宣言 --- */
	clock_t start_clock_c, end_clock_c;
	clock_t start_clock_neon, end_clock_neon;
	char* src=NULL;
	char* dst[3]={NULL, NULL, NULL};
	
	/* --- 引数処理 --- */
	show_usage();
	
	/* --- RGBピクセル値取得：C言語 --- */
	start_clock_c = clock();
	rgb_deinterleave_c(src, dst);
	end_clock_c = clock();
	
	/* --- RGBピクセル値取得：Neon --- */
	start_clock_neon = clock();
	rgb_deinterleave_neon(src, dst);
	end_clock_neon = clock();
	
	/* --- 処理速度表示 --- */
	MY_PRINT(MY_PRINT_LVL_INFO, "[Processing Duration]\n");
	MY_PRINT(MY_PRINT_LVL_INFO, "function, start_clock, end_clock, end-start\n");
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_c, %ld, %ld, %ld\n", start_clock_c, end_clock_c, end_clock_c-start_clock_c);
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_neon, %ld, %ld, %ld\n", start_clock_neon, end_clock_neon, end_clock_neon-start_clock_neon);
	

	return 0;
}

