/**
 * @file main.c
 * @brief テスト用データを生成するツール
 */

#include "common.h"
#include "generate_test_data.h"

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
int show_usage()
{
	printf("<< Usage >>\n");
	printf("  ./generate_test_data <file_size> <output_file>\n");
	printf("    file_size: ファイルサイズ[byte]\n");
	printf("    output_file: 出力ファイル\n");

	return 0;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details テスト用データを生成する
 */
int main(int argc, char* argv[])
{
	/* --- 変数宣言 --- */
	FILE* fDst;
	char* strFileName;
	int iFileSize;
	
	/* --- 引数処理 --- */
	if (argc != 3) {
		show_usage();
		return -1;
	} else {
		iFileSize = atoi(argv[1]);
		strFileName = argv[2];
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "[Variables]\n");
	MY_PRINT(MY_PRINT_LVL_INFO, "  * file_size = %d\n", iFileSize);
	MY_PRINT(MY_PRINT_LVL_INFO, "  * output_file = %s\n", strFileName);
	
	/* --- テスト用データ生成 --- */
	fDst = fopen(strFileName, "wb");
	if (fDst != NULL) {
		generate_test_data(fDst, iFileSize);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file: %s\n", strFileName);
		return -1;
	}
	
	fclose(fDst);
	return 0;
}

