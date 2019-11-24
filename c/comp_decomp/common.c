/**
 * @file common.c
 * @brief 共通処理
 */

#include "common.h"


/**
 * @brief srcからデータを読み出す
 * @param[in,out] get_bits_param ビット取得処理用パラメータ @n
 *                               read_dataに取得データを格納する
 * @param[in] read_only リードポインタの更新有無を指定する @n
 *                      - GET_BITS_FALSE : リードポインタを更新しない (データの先読み時などで使用) @n
 *                      - GET_BITS_TRUE : リードポインタを更新する
 * @return int 0:エラーなしで終了，-1:処理中にエラー発生
 * @details srcからデータを読み出す
 */
int get_bits(GET_BITS_PARAM *get_bits_param, GET_BITS_FLAG read_only)
{
	int ret = 0;
	int remain_bits = 8-get_bits_param->bit_ptr;
	unsigned char mask = ((1 << remain_bits) - 1);
	int iter;
	
	iter = get_bits_param->byte_ptr;
	if (remain_bits >= get_bits_param->read_size) {
		mask &= ~((1 << (remain_bits - get_bits_param->read_size)) - 1);
		get_bits_param->read_data = (get_bits_param->src[iter] & mask) >> (remain_bits - get_bits_param->read_size);
	} else {
		get_bits_param->read_data = get_bits_param->src[iter++] & mask;
		for (; iter <= get_bits_param->byte_ptr + ((get_bits_param->read_size - remain_bits) / 8); iter++) {
			get_bits_param->read_data = (get_bits_param->read_data << 8) |
							get_bits_param->src[iter];
		}
		remain_bits = (get_bits_param->read_size - remain_bits) % 8;
		if (remain_bits > 0) {
			get_bits_param->read_data = (get_bits_param->read_data << remain_bits) |
							((get_bits_param->src[iter] >> (8 - remain_bits)) & ((1 << remain_bits) - 1));
		}
	}

	if (!read_only) {
		get_bits_param->byte_ptr += get_bits_param->read_size / 8;
		get_bits_param->bit_ptr += get_bits_param->read_size % 8;
		if (get_bits_param->bit_ptr >= 8) {
			get_bits_param->bit_ptr -= 8;
			get_bits_param->byte_ptr += 1;
		}
	}

	return ret;
}

/**
 * @brief dstへデータを書き出す
 * @param[in] put_bits_param ビット取得処理用パラメータ
 * @return int 0:エラーなしで終了，-1:処理中にエラー発生
 * @details dstへデータを書き出す
 */
int put_bits(PUT_BITS_PARAM* put_bits_param)
{
	int ret = 0;
	unsigned int write_data;
	int write_byte;
	int remain_bits;
	int iter;

	write_data = (*(put_bits_param->dst+put_bits_param->byte_ptr) << 24) |
			(put_bits_param->put_data << (32-put_bits_param->put_size-put_bits_param->bit_ptr));
	write_byte = MIN(4, (put_bits_param->put_size+put_bits_param->bit_ptr)/8);
	*(put_bits_param->dst + put_bits_param->byte_ptr) = (write_data >> 24) & 0xff;
	for (iter = 1; iter < write_byte; iter++) {
		*(put_bits_param->dst + put_bits_param->byte_ptr + iter) = (write_data >> (24 - iter*8)) & 0xff;
	}
	if (iter > 0) {
		put_bits_param->byte_ptr += write_byte;
	}

	if ((put_bits_param->put_size + put_bits_param->bit_ptr) > 32) {
		remain_bits = 32 - (put_bits_param->put_size + put_bits_param->bit_ptr);
		write_data = (put_bits_param->put_data & ((1 << remain_bits) - 1) << (8 - remain_bits));
		*(put_bits_param->dst + put_bits_param->byte_ptr) = write_data & 0xff;
		put_bits_param->byte_ptr += 1;
	}
	put_bits_param->bit_ptr += put_bits_param->put_size % 8;
	if (put_bits_param->bit_ptr >= 8) {
		put_bits_param->bit_ptr -= 8;
	}

	return ret;
}

