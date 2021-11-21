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
	printf("  ./rgb_deinterleave <rgb_binary_file>\n");
	printf("    rgb_binary_file: RGBデータ\n");
	printf("    rgb_binary_file_size: RGBデータ\n");

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
	FILE* fpBinFile;
	clock_t start_clock_c, end_clock_c;
	clock_t start_clock_neon, end_clock_neon;
	char* strBinFileName;
	unsigned char* src=NULL;
	unsigned char* dst[3]={NULL, NULL, NULL};
	int iBinReadSize;
	int i;
	
	/* --- 引数処理 --- */
	if (argc != 3) {
		show_usage();
		return -1;
	} else {
		strBinFileName = argv[1];
		iBinReadSize = (int)(atoi(argv[2]) / 3) * 3;	// 3の倍数に切り捨て
	}
	
	fpBinFile = fopen(strBinFileName, "wb");
	src = (unsigned char*)malloc(iBinReadSize);
	fread(src, 1, iBinReadSize, fpBinFile);
	fclose(fpBinFile);
	
	for (i = 0; i < 3; i++) {
		dst[i] = (unsigned char*)malloc(iBinReadSize / 3);
	}
	
	/* --- RGBピクセル値取得：C言語 --- */
	start_clock_c = clock();
	rgb_deinterleave_c(src, iBinReadSize, dst);
	end_clock_c = clock();
	
	/* --- RGBピクセル値取得：Neon --- */
	start_clock_neon = clock();
	rgb_deinterleave_neon(src, iBinReadSize, dst);
	end_clock_neon = clock();
	
	/* --- 処理速度表示 --- */
	MY_PRINT(MY_PRINT_LVL_INFO, "[Processing Duration]\n");
	MY_PRINT(MY_PRINT_LVL_INFO, "function, start_clock, end_clock, end-start\n");
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_c, %ld, %ld, %ld\n", start_clock_c, end_clock_c, end_clock_c-start_clock_c);
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_neon, %ld, %ld, %ld\n", start_clock_neon, end_clock_neon, end_clock_neon-start_clock_neon);
	

	free(src);
	for (i = 0; i < 3; i++) {
		free(dst[i]);
	}
	return 0;
}

