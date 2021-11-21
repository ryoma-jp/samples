/**
 * @file generate_test_data.c
 * @brief テスト用データを生成する
 */

#include "common.h"
#include "generate_test_data.h"

/**
 * @brief テスト用データを生成する
 * @param output_file テスト用データ保存先のファイル
 * @param file_size テスト用データのサイズ[byte]
 * @return int 0固定
 * @details テスト用データを生成する
 */
int generate_test_data(FILE* output_file, int file_size)
{
	int i;
	char* data = (char*)malloc(file_size);
	
	for (i = 0; i < file_size; i++) {
		data[i] = i & 0xFF;
	}
	fwrite(data, 1, file_size, output_file);
	
	return 0;
}


