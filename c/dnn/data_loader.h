
#ifndef __DATA_LOADER_H__
#define __DATA_LOADER_H__

/**
 * @struct tImgParams
 * @brief 画像データパラメータ
 */
typedef struct _tImgData {
	unsigned int height;
	unsigned int width;
	unsigned int channel;
	unsigned char* data;
} tImgData;


extern int load_bin_file(char* byte_file, tImgData* dst);

#endif /*__DATA_LOADER_H__ */
