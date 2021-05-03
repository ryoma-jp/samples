/**
 * @file data_loader.c
 * @brief byteデータで固められたfloatデータを読み込むサンプル
 */

#include "data_loader.h"
#include <common.h>

/**
 * @brief byteデータファイルを読み込む
 * @return int 0固定
 * @details byteデータファイルを読み込む
 */
int load_bin_file(char* byte_file, tImgData* dst)
{
	FILE* fpByteFile;
	unsigned int read_data;
	unsigned int n_data;
	unsigned int d_type;
	float f_val;
	int i;

	/* --- file open --- */
	fpByteFile = fopen(byte_file, "rb");
	
	/* --- load n_data --- */
	fread(&n_data, 4, 1, fpByteFile);
	
	/* --- load d_type --- */
	fread(&d_type, 4, 1, fpByteFile);
	
	/* --- load data --- */
	if (d_type == 0) {
		/* --- Image Data --- */
		dst->data = (unsigned char*)malloc(n_data * sizeof(float));
		
		fread(&(dst->height), 4, 1, fpByteFile);
		fread(&(dst->width), 4, 1, fpByteFile);
		fread(&(dst->channel), 4, 1, fpByteFile);
		
		for (i = 0; i < n_data; i++) {
			fread(&read_data, 4, 1, fpByteFile);
			memcpy(dst->data + (i << 2), &read_data, 4);
		}
	} else {
		/* --- T.B.D --- */
	}
	
	fclose(fpByteFile);

	return 0;
}

