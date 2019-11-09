/**
 * @file main.c
 * @brief 圧縮・解凍アルゴリズムのサンプル
 */

#include "runlength.h"
#include "huffman.h"
#include "common.h"
#include <string.h>

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
static int show_usage()
{
	printf("<< Usage >>\n");
	printf("  ./comp_decomp [flag] [input_file] [output_file]\n");
	printf("    flag : エンコード処理またはデコード処理を選択するフラグ\n");
	printf("             --dec : デコード\n");
	printf("             --enc : エンコード\n");
	printf("    input_file : エンコードまたはデコード対象のファイル\n");
	printf("    output_file : エンコードまたはデコード結果を出力するファイル\n");

	return 0;
}

/**
 * @enum _DEC_ENC_MODE
 * @brief エンコード処理またはデコード処理を示す
 */
typedef enum _DEC_ENC_MODE {
	DEC_MODE,
	ENC_MODE,
	ERROR
} DEC_ENC_MODE;

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数 @n
 *              argv[1] : flag エンコード処理またはデコード処理を選択するフラグ @n
 *              argv[2] : input_file エンコードまたはデコード対象のファイル @n
 *              argv[3] : output_file エンコードまたはデコード結果を出力するファイル
 * @return int 0固定
 * @details flagの指示にもとづきinput_fileをエンコードまたはデコードしoutput_fileへ出力する
 */
int main(int argc, char* argv[])
{
	DEC_ENC_MODE dec_enc_mode;
	FILE* fp_input;
	FILE* fp_output;
	char* src_buf;
	char* dst_buf;
	RUNLENGTH_ENC_PARAMS enc_params;

	if (argc != 4) {
		show_usage();
		exit(0);
	}

	if (strcmp(argv[1], "--dec") == 0) {
		dec_enc_mode = DEC_MODE;
	} else if (strcmp(argv[1], "--enc") == 0) {
		dec_enc_mode = ENC_MODE;
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Unknown mode\n");
		exit(0);
	}

	fp_input = fopen(argv[2], "r");
	if (fp_input == NULL) {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", argv[2]);
		exit(0);
	}

	fp_output = fopen(argv[2], "w");
	if (fp_output == NULL) {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", argv[3]);
		exit(0);
	}

	src_buf = (char*)malloc(1024*1024);	/* T.B.D */
	dst_buf = (char*)malloc(1024*1024);	/* T.B.D */

	switch (dec_enc_mode) {
		case DEC_MODE:
			break;
		case ENC_MODE:
			enc_params.src = src_buf;
			enc_params.src_len = 1024 * 1024;
			enc_params.enc_unit = 8;
			enc_params.enc_len_unit = 8;
			enc_params.dst = dst_buf;
			enc_params.dst_len = 1024 * 1024;
			enc_params.header = NULL;
			runlength_encode(enc_params);

			printf("[DEBUG] %d, %d\n", dst_buf[0], dst_buf[1]);
			break;
		default:
			break;
	}

	fclose(fp_input);
	fclose(fp_output);
	free(src_buf);
	free(dst_buf);

	return 0;
}

