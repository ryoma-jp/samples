
#ifndef __DATA_LOADER_H__
#define __DATA_LOADER_H__

#include <stdio.h>
#include <stdlib.h>

/**
 * @enum DATA_TYPE
 * @brief データ種別
 * @par
 *   - DATA_TYPE_IMG_UINT8: 1ピクセルを8bitで表現する画像データ
 *   - DATA_TYPE_IMG_FLOAT: 1ピクセルを32bit(float)で表現する画像データ
 */
typedef enum _DATA_TYPE {
	DATA_TYPE_IMG_UINT8 = 0,
	DATA_TYPE_IMG_FLOAT = 1,
} DATA_TYPE;

/**
 * @struct tImgParams
 * @brief 画像データパラメータ
 */
typedef struct _tImgData {
	DATA_TYPE d_type;
	unsigned int height;
	unsigned int width;
	unsigned int channel;
	union {
		unsigned char* img_uint8;	// DATA_TYPE_IMG_UINT8
		float* img_float;		// DATA_TYPE_IMG_FLOAT
	} data;
} tImgData;


extern unsigned int get_data_size(FILE* byte_file);
extern int load_bin_file(FILE* byte_file, void* dst);

#endif /*__DATA_LOADER_H__ */

