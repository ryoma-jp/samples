/**
 * @file main.c
 * @brief float2byteで出力したバイナリファイルを読み込むサンプル
 */

#include <read_sample_c.h>
#include <common.h>

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
int show_usage()
{
	printf("<< Usage >>\n");
	printf("  float2byteで出力したバイナリファイルを読み込むサンプル\n");
	printf("  ./read_sample_c <bin_file> <n_data>\n");
	printf("    bin_file: float2byteで出力したバイナリファイル\n");
	printf("    n_data: バイナリファイル内のfloatデータ数\n");

	return 0;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details float2byteで出力したバイナリファイルを読み込むサンプル
 */
int main(int argc, char* argv[])
{
	/* --- 変数宣言 --- */
	char* byte_file;
	int n_data;

	/* --- 引数取り込み --- */
	if (argc != 3) {
		show_usage();
		exit(0);
	} else {
		byte_file = argv[1];
		n_data = atoi(argv[2]);
	}

	rsc_read_file(byte_file, n_data);

	return 0;
}

