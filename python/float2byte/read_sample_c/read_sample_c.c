/**
 * @file read_sample_c.c
 * @brief byteデータで固められたfloatデータを読み込むサンプル
 */

#include <read_sample_c.h>
#include <common.h>

/**
 * @brief byteデータファイルを読み込む
 * @return int 0固定
 * @details byteデータファイルを読み込む
 */
int rsc_read_file(char* byte_file, int n_data)
{
	FILE* fpByteFile;
	unsigned int read_data;
	float f_val;
//	float f_val2;
	int i;

	fpByteFile = fopen(byte_file, "rb");

	for (i = 0; i < n_data; i++) {
		fread(&read_data, 4, 1, fpByteFile);
		memcpy(&f_val, &read_data, 4);
//		MY_PRINT(MY_PRINT_LVL_INFO, "read_data = %x\n", read_data);
		MY_PRINT(MY_PRINT_LVL_INFO, "f_val[%03d] = %f\n", i, f_val);
	}

/*
	f_val2 = 0.1;
	MY_PRINT(MY_PRINT_LVL_INFO, "f_val2 = %f\n", f_val2);
	for (i = 0; i < 4; i++) {
		printf("%02x\n", *((unsigned char*)(&f_val2) + i));
	}
*/
	
	fclose(fpByteFile);

	return 0;
}

