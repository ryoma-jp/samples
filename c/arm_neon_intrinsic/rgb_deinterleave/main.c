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
	unsigned char* dst_c[3]={NULL, NULL, NULL};
	unsigned char* dst_neon[3]={NULL, NULL, NULL};
	int iBinReadSize;
	int i, j;
	
	/* --- 引数処理 --- */
	if (argc != 3) {
		show_usage();
		return -1;
	} else {
		strBinFileName = argv[1];
		iBinReadSize = (int)(atoi(argv[2]) / 3) * 3;	// 3の倍数に切り捨て
	}
	
	fpBinFile = fopen(strBinFileName, "rb");
	src = (unsigned char*)malloc(iBinReadSize);
	fread(src, 1, iBinReadSize, fpBinFile);
	fclose(fpBinFile);
	
	for (i = 0; i < 3; i++) {
		/* --- 16byteアラインで領域を確保 --- */
		dst_c[i] = (unsigned char*)malloc((int)(iBinReadSize / 3 / 16) * 16 + 16);
		dst_neon[i] = (unsigned char*)malloc((int)(iBinReadSize / 3 / 16) * 16 + 16);
	}
	
	/* --- RGBピクセル値取得：C言語 --- */
	start_clock_c = clock();
	rgb_deinterleave_c(src, iBinReadSize, dst_c);
	end_clock_c = clock();
	
	/* --- RGBピクセル値取得：Neon --- */
	start_clock_neon = clock();
	rgb_deinterleave_neon(src, iBinReadSize, dst_neon);
	end_clock_neon = clock();
	
	/* --- 処理結果の照合 --- */
	for (i = 0; i < 3; i++) {
		for (j = 0; j < (iBinReadSize / 3); j++) {
			if (dst_c[i][j] != dst_neon[i][j]) {
				MY_PRINT(MY_PRINT_LVL_ERROR, "dst_c[%d][%d] != dst_neon[%d][%d] (0x%02x, 0x%02x)\n",
					i, j, i, j, dst_c[i][j], dst_neon[i][j]);
			}
		}
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "[Verification is Passed] dst_c == dst_neon\n")
	
	/* --- 処理速度表示 --- */
	MY_PRINT(MY_PRINT_LVL_INFO, "[Processing Duration]\n");
	MY_PRINT(MY_PRINT_LVL_INFO, "function, start_clock, end_clock, end-start\n");
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_c, %ld, %ld, %ld\n", start_clock_c, end_clock_c, end_clock_c-start_clock_c);
	MY_PRINT(MY_PRINT_LVL_INFO, "rgb_deinterleave_neon, %ld, %ld, %ld\n", start_clock_neon, end_clock_neon, end_clock_neon-start_clock_neon);
	
	free(src);
	for (i = 0; i < 3; i++) {
		free(dst_c[i]);
		free(dst_neon[i]);
	}
	return 0;
}

