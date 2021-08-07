/**
 * @file data_loader.c
 * @brief byteデータで固められたfloatデータを読み込むサンプル
 * @par
 *  - byteデータは"tools/img2byte"を使用して生成することが可能
 *  - byteデータフォーマット
 *      - data_size (4bytes) データサイズ[byte]
 *      - d_type (4bytes) データ種別(0: 画像データ)
 *          - 0: 画像データ(pixel;UINT8)
 *          - 1: 画像データ(正規化;float)
 *      - data (data_size bytes) データ
 *          - 画像データ(pixel;UINT8)の場合
 *              - height (4bytes) 画像の高さ
 *              - width (4bytes) 画像の幅
 *              - channel (4bytes) チャネル数(1: グレースケール, 3: カラー(RGB/BGRは考慮しない))
 *              - data (data_size-12 bytes) 画素データ
 *          - 画像データ(正規化;float)の場合
 *              - height (4bytes) 画像の高さ
 *              - width (4bytes) 画像の幅
 *              - channel (4bytes) チャネル数(1: グレースケール, 3: カラー(RGB/BGRは考慮しない))
 *              - data (data_size-12 bytes) 画素データ
 */

#include "data_loader.h"
#include <common.h>

/**
 * @brief byteデータファイルのデータサイズを取得する
 * @param byte_file byteデータファイル
 * @return unsigned int データサイズ
 */
unsigned int get_data_size(FILE* byte_file)
{
	unsigned int data_size;
	unsigned int d_type;
	long file_pos;

	/* --- get current file position --- */
	file_pos = ftell(byte_file);

	/* --- load data_size --- */
	fread(&data_size, 4, 1, byte_file);

	/* --- load d_type --- */
	fread(&d_type, 4, 1, byte_file);
	
	/* --- load data --- */
	if ((d_type == DATA_TYPE_IMG_UINT8) || (d_type == DATA_TYPE_IMG_FLOAT)) {
		data_size = data_size - 12;
	} else {
		/* --- T.B.D --- */
	}

	/* --- get previous file position --- */
	fseek(byte_file, SEEK_SET, file_pos);

	return data_size;
}

/**
 * @brief byteデータファイルを読み込む
 * @param byte_file byteデータファイル
 * @param dst 読み込んだデータを格納するバッファ
 * @return int 0固定
 * @details byteデータファイルを読み込む
 */
int load_bin_file(FILE* byte_file, void* dst)
{
	union _dst_buf {
		tImgData* img_data;
	} dst_buf;
	unsigned int read_data;
	unsigned int data_size;
	unsigned int d_type;
	float f_val;
	int i;

	/* --- load data_size --- */
	fread(&data_size, 4, 1, byte_file);
	
	/* --- load d_type --- */
	fread(&d_type, 4, 1, byte_file);
	
	/* --- load data --- */
	if (d_type == 0) {
		/* --- 出力先バッファ --- */
		dst_buf.img_data = (tImgData*)dst;

		/* --- d_type --- */
		dst_buf.img_data->d_type = (DATA_TYPE)(d_type);

		/* --- Image Shape --- */
		fread(&(dst_buf.img_data->height), 4, 1, byte_file);
		fread(&(dst_buf.img_data->width), 4, 1, byte_file);
		fread(&(dst_buf.img_data->channel), 4, 1, byte_file);

		/* --- Image Data --- */
		fread(dst_buf.img_data->data.img_uint8, data_size - 12, 1, byte_file);
	} else {
		/* --- T.B.D --- */
	}
	
	return 0;
}

