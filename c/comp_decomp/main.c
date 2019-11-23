/**
 * @file main.c
 * @brief 圧縮・解凍アルゴリズムのサンプル
 */

#include "runlength.h"
#include "huffman.h"
#include "common.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

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
	printf("    enc_unit (エンコード時のみ指定) 符号化単位(ビット数で指定，最大32)\n");
	printf("    enc_len_unit (エンコード時のみ指定) 連長ビット数(最大32)\n");

	return 0;
}

/**
 * @enum _DEC_ENC_MODE
 * @brief エンコード処理またはデコード処理を示す
 */
typedef enum _DEC_ENC_MODE {
	DEC_MODE,	//!< デコード処理
	ENC_MODE,	//!< エンコード処理
	ERROR		//!< エラー
} DEC_ENC_MODE;

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数 @n
 *              argv[1] : flag エンコード処理またはデコード処理を選択するフラグ @n
 *              argv[2] : input_file エンコードまたはデコード対象のファイル @n
 *              argv[3] : output_file エンコードまたはデコード結果を出力するファイル @n
 *              argv[4] : enc_unit (エンコード時のみ指定) 符号化単位(ビット数で指定，最大32) @n
 *              argv[5] : enc_len_unit (エンコード時のみ指定) 連長ビット数(最大32)
 * @return int 0固定
 * @details flagの指示にもとづきinput_fileをエンコードまたはデコードしoutput_fileへ出力する
 */
int main(int argc, char* argv[])
{
	DEC_ENC_MODE dec_enc_mode;
	FILE* fp_input;
	FILE* fp_output;
	unsigned int src_size;
	char* src_buf;
	char* dst_buf;
	RUNLENGTH_ENC_PARAMS enc_params;
	RUNLENGTH_DEC_PARAMS dec_params;
	int fd_input;
	struct stat stbuf_input;
	int dst_len;
	int enc_unit;
	int enc_len_unit;

	if (strcmp(argv[1], "--dec") == 0) {
		if (argc != 4) {
			show_usage();
			exit(0);
		} else {
			dec_enc_mode = DEC_MODE;
		}
	} else if (strcmp(argv[1], "--enc") == 0) {
		if (argc != 6) {
			show_usage();
			exit(0);
		} else {
			dec_enc_mode = ENC_MODE;
		}
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Unknown mode\n");
		exit(0);
	}

	fd_input = open(argv[2], O_RDONLY);
	if (fd_input == -1) {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", argv[2]);
		exit(0);
	}
	fp_input = fdopen(fd_input, "rb");
	if (fp_input == NULL) {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", argv[2]);
		exit(0);
	}

	if (fstat(fd_input, &stbuf_input) == -1) {
		MY_PRINT(MY_PRINT_LVL_ERROR, "fstat() failed\n");
		exit(0);
	}
	src_size = stbuf_input.st_size;

	fp_output = fopen(argv[3], "wb");
	if (fp_output == NULL) {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", argv[3]);
		exit(0);
	}

	switch (dec_enc_mode) {
		case DEC_MODE:
			src_buf = (char*)malloc(src_size);
			dst_buf = (char*)malloc(src_size);	/* T.B.D:src_sizeと同じサイズを確保 */
			fread(src_buf, 1, src_size, fp_input);

			dec_params.src = src_buf;
			dec_params.src_len = src_size;
			dec_params.dst = dst_buf;
			dec_params.header = NULL;
			dst_len = runlength_decode(dec_params);

			fwrite(dst_buf, 1, dst_len, fp_output);

			break;
		case ENC_MODE:
			enc_unit = atoi(argv[4]);
			if ((enc_unit < 1) && (enc_unit > 32)) {
				MY_PRINT(MY_PRINT_LVL_ERROR, "enc_unit must set to under 32bit\n");
				exit(0);
			}
			enc_len_unit = atoi(argv[5]);
			if ((enc_len_unit < 1) && (enc_len_unit > 32)) {
				MY_PRINT(MY_PRINT_LVL_ERROR, "enc_len_unit must set to under 32bit\n");
				exit(0);
			}

			src_buf = (char*)malloc(src_size);
			dst_buf = (char*)malloc(src_size * (enc_len_unit / enc_unit + 1));
			fread(src_buf, 1, src_size, fp_input);

			enc_params.src = src_buf;
			enc_params.src_len = src_size;
			enc_params.enc_unit = enc_unit;
			enc_params.enc_len_unit = enc_len_unit;
			enc_params.dst = dst_buf;
			enc_params.header = NULL;
			dst_len = runlength_encode(enc_params);

			fwrite(dst_buf, 1, dst_len, fp_output);
			break;
		default:
			break;
	}

	close(fd_input);
	fclose(fp_output);
	free(src_buf);
	free(dst_buf);

	return 0;
}

