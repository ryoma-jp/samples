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
	printf("  ./comp_decomp [proc_type] [input_file] [output_file]\n");
	printf("    proc_type : エンコード処理またはデコード処理を選択するフラグ\n");
	printf("             --rl_dec : ランレングスデコード\n");
	printf("             --fm_dec : ハフマンデコード\n");
	printf("             --rl_enc : ランレングスエンコード\n");
	printf("             --fm_enc : ハフマンエンコード\n");
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
	RUNLENGTH_DEC_MODE,	//!< ランレングスデコード処理
	HUFFMAN_DEC_MODE,	//!< ハフマンデコード処理
	RUNLENGTH_ENC_MODE,	//!< ランレングスエンコード処理
	HUFFMAN_ENC_MODE,	//!< ハフマンエンコード処理
	ERROR		//!< エラー
} DEC_ENC_MODE;

/**
 * @brief proc_typeをチェックする関数
 * @param[in] proc_type 処理種別
 * @return DEC_ENC_MODE 処理モード
 * @details proc_typeの指示にもとづき処理モードを返す
 */
static DEC_ENC_MODE check_proc_type(char* proc_type)
{
	DEC_ENC_MODE dec_enc_mode = ERROR;

	if (strcmp(proc_type, "--rl_dec") == 0) {
		dec_enc_mode = RUNLENGTH_DEC_MODE;
	} else if (strcmp(proc_type, "--rl_enc") == 0) {
		dec_enc_mode = RUNLENGTH_ENC_MODE;
	} else if (strcmp(proc_type, "--fm_dec") == 0) {
		dec_enc_mode = HUFFMAN_DEC_MODE;
	} else if (strcmp(proc_type, "--fm_enc") == 0) {
		dec_enc_mode = HUFFMAN_ENC_MODE;
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Unknown mode\n");
		exit(0);
	}

	return dec_enc_mode;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数 @n
 *              argv[1] : proc_type エンコード処理またはデコード処理を選択するフラグ @n
 *              argv[2] : input_file エンコードまたはデコード対象のファイル @n
 *              argv[3] : output_file エンコードまたはデコード結果を出力するファイル @n
 *              argv[4] : enc_unit (エンコード時のみ指定) 符号化単位(ビット数で指定，最大32) @n
 *              argv[5] : enc_len_unit (エンコード時のみ指定) 連長ビット数(最大32) ※ランレングスエンコード時
 * @return int 0固定
 * @details proc_typeの指示にもとづきinput_fileをエンコードまたはデコードしoutput_fileへ出力する
 */
int main(int argc, char* argv[])
{
	DEC_ENC_MODE dec_enc_mode;
	FILE* fp_input = NULL;
	FILE* fp_output = NULL;
	unsigned int src_size;
	char* src_buf = NULL;
	char* dst_buf = NULL;
	RUNLENGTH_ENC_PARAMS runlength_enc_params;
	RUNLENGTH_DEC_PARAMS runlength_dec_params;
	HUFFMAN_ENC_PARAMS huffman_enc_params;
	HUFFMAN_DEC_PARAMS huffman_dec_params;
	int fd_input;
	struct stat stbuf_input;
	int dst_len;
	int enc_unit;
	int enc_len_unit;

	dec_enc_mode = check_proc_type(argv[1]);
	switch (dec_enc_mode) {
		case RUNLENGTH_DEC_MODE:
		case HUFFMAN_DEC_MODE:
			if (argc != 4) {
				show_usage();
				exit(0);
			}
			break;
		case RUNLENGTH_ENC_MODE:
			if (argc != 6) {
				show_usage();
				exit(0);
			}
			break;
		case HUFFMAN_ENC_MODE:
			if (argc != 5) {
				show_usage();
				exit(0);
			}
			break;
		default:
			show_usage();
			exit(0);
			break;
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
		case RUNLENGTH_DEC_MODE:
			src_buf = (char*)malloc(src_size);
			dst_buf = (char*)malloc(src_size);	/* T.B.D:src_sizeと同じサイズを確保 */
			fread(src_buf, 1, src_size, fp_input);

			runlength_dec_params.src = src_buf;
			runlength_dec_params.src_len = src_size;
			runlength_dec_params.dst = dst_buf;
			runlength_dec_params.header = NULL;
			dst_len = runlength_decode(runlength_dec_params);

			fwrite(dst_buf, 1, dst_len, fp_output);

			break;
		case RUNLENGTH_ENC_MODE:
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

			runlength_enc_params.src = src_buf;
			runlength_enc_params.src_len = src_size;
			runlength_enc_params.enc_unit = enc_unit;
			runlength_enc_params.enc_len_unit = enc_len_unit;
			runlength_enc_params.dst = dst_buf;
			runlength_enc_params.header = NULL;
			dst_len = runlength_encode(runlength_enc_params);

			fwrite(dst_buf, 1, dst_len, fp_output);
			break;
		case HUFFMAN_DEC_MODE:
			src_buf = (char*)malloc(src_size);
			dst_buf = (char*)malloc(src_size);	/* T.B.D:src_sizeと同じサイズを確保 */
			fread(src_buf, 1, src_size, fp_input);

			huffman_dec_params.src = src_buf;
			huffman_dec_params.src_len = src_size;
			huffman_dec_params.dst = dst_buf;
			huffman_dec_params.header = NULL;
			dst_len = huffman_decode(huffman_dec_params);

			fwrite(dst_buf, 1, dst_len, fp_output);

			break;
		case HUFFMAN_ENC_MODE:
			enc_unit = atoi(argv[4]);
			if ((enc_unit < 1) && (enc_unit > 32)) {
				MY_PRINT(MY_PRINT_LVL_ERROR, "enc_unit must set to under 32bit\n");
				exit(0);
			}

			src_buf = (char*)malloc(src_size);
			dst_buf = (char*)malloc(src_size);	/* T.B.D : エンコード結果のサイズは暫定 */
			fread(src_buf, 1, src_size, fp_input);

			huffman_enc_params.src = src_buf;
			huffman_enc_params.src_len = src_size;
			huffman_enc_params.enc_unit = enc_unit;
			huffman_enc_params.dst = dst_buf;
			huffman_enc_params.header = NULL;
			dst_len = huffman_encode(huffman_enc_params);

			fwrite(dst_buf, 1, dst_len, fp_output);
			break;
		default:
			MY_PRINT(MY_PRINT_LVL_ERROR, "Unkown dec_enc_mode : %d\n", dec_enc_mode);
			break;
	}


	close(fd_input);
	fclose(fp_output);
	if (src_buf != NULL) {
		free(src_buf);
	}
	if (dst_buf != NULL) {
		free(dst_buf);
	}

	return 0;
}

