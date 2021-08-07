/**
 * @file main.c
 * @brief DNNの推論を実行するプログラム
 */

#include <data_loader.h>
#include <common.h>

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
int show_usage()
{
	printf("<< Usage >>\n");
	printf("  DNNの推論を実行するプログラム\n");
	printf("  ./dnn_inference <input_data>\n");
	printf("    input_data: バイナリ形式の入力データ\n");

	return 0;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details DNNの推論を実行する
 */
int main(int argc, char* argv[])
{
	/* --- 変数宣言 --- */
	FILE* fp_byte_file;
	char* byte_file;
	tImgData image_data;
	unsigned int data_size;
	
	/* --- 引数取り込み --- */
	if (argc != 2) {
		show_usage();
		exit(0);
	} else {
		byte_file = argv[1];
		printf("[INFO] byte_file: %s\n", byte_file);
	}
	
	/* --- データ読み込み --- */
	fp_byte_file = fopen(byte_file, "rb");
	data_size = get_data_size(fp_byte_file);
	image_data.data.img_uint8 = (unsigned char*)malloc(data_size);

	load_bin_file(fp_byte_file, &image_data);
	printf("[INFO] d_type=%d\n", image_data.d_type);
	printf("[INFO] height=%d\n", image_data.height);
	printf("[INFO] width=%d\n", image_data.width);
	printf("[INFO] channel=%d\n", image_data.channel);
	fclose(fp_byte_file);

	free(image_data.data.img_uint8);
	return 0;
}

