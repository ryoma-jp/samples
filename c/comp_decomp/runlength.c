/**
 * @file runlength.c
 * @brief ランレングスデコード・エンコード
 *   - 同じ情報が続く場合に連長と情報の内容を用いて圧縮を実現する @n
 *       [例] @n
 *       aaaaabccdddeeee	15文字 @n
 *       → a5b1c2d3e4		10文字：5文字圧縮 @n
 *   - 上記の場合，b(1文字)→b1(2文字)となり情報量が増加する為，情報全てを連長と情報で表現する場合は必ずしも圧縮できるとは限らない @n
 *     圧縮部分とそうでない部分を制御文字を用いて区別することで，情報量の増加を抑制できる @n
 *      [制御文字に@を用いる例] @n
 *      aaaaabccdddeeee		15文字 @n
 *      → \@a5bccddd\@e4	12文字：3文字圧縮 @n
 *     - 圧縮対象のデータに含まれない制御文字を選択する必要がある @n
 *       あるいは，エスケープシーケンス(\)などで区別できるようにする仕組みが必要である @n
 *       ※ただし，エスケープシーケンスを使うと情報量増加の抑制ができなくなる @n
 *   - 圧縮単位や連長の選択も重要 @n
 *       [例1] @n
 *       圧縮対象データ：abcabcabc            9文字 @n
 *       圧縮単位 1文字：a1b1c1a1b1c1a1b1c1   18文字 @n
 *       圧縮単位 3文字：abc3                 4文字 @n
 *       [例2] @n
 *       圧縮対象データ：aaaaaaaaaaaaaaa      15文字 @n
 *       連長 1文字：a9a6                     4文字 @n
 *       連長 2文字：a15                      3文字 @n
 *   - エンコードしたデータのデコード結果を格納するバッファサイズを決めるために， @n
 *     エンコード結果のヘッダにデコード後のデータサイズを格納しておく
 *   - 本プログラムの仕様 @n
 *     - 圧縮対象のデータの並びに依存して制御文字の有効性が変動する為， @n
 *       制御文字は使用せず，ランレングスデコード・エンコードはすべてのデータを対象とする @n
 *     - 圧縮単位及び連長桁は圧縮とともにヘッダとして保存できる仕様とする @n
 *     - ヘッダの仕様
 *       - header[0:7]  : 圧縮単位[bit数]
 *       - header[8:15] : 連長[bit数]
 *       - header[16:31] : デコード後のデータサイズ
 *     - ヘッダは圧縮後データに連結する仕様と分離する仕様を選択できるものとする @n
 *     - なお，適切な圧縮単位・連長桁を探索する仕組みは実装しない [T.B.D]
 */

#include "runlength.h"
#include "common.h"

/**
 * @struct _RUNLENGTH_GET_BITS_PARAM
 * @brief ビット取得処理用パラメータ
 */
typedef struct _RUNLENGTH_GET_BITS_PARAM {
	char* src;		//!< データを読み出すバッファ
	unsigned int read_data;	//!< 取得データ
	int read_size;		//!< 取得データのサイズ(32bit以下をbit単位で指定)
	unsigned int byte_ptr;	//!< バイト単位のリードポインタ
	unsigned int bit_ptr;	//!< byte_ptr内のビット位置を示すリードポインタ
} RUNLENGTH_GET_BITS_PARAM;

/**
 * @brief srcからデータを読み出す
 * @param[in,out] get_bits_param ビット取得処理用パラメータ @n
 *                               read_dataに取得データを格納する
 * @return RUNLENGTH_RET
 * @details srcからデータを読み出す
 */
static RUNLENGTH_RET get_bits(RUNLENGTH_GET_BITS_PARAM *get_bits_param)
{
	RUNLENGTH_RET ret;

	return ret;
}

/**
 * @struct _RUNLENGTH_PUT_BITS_PARAM
 * @brief ビット書き込み処理用パラメータ
 */
typedef struct _RUNLENGTH_PUT_BITS_PARAM {
	char* dst;		//!< 書き込み先のバッファ
	unsigned int put_data;	//!< 書き込むデータ
	int put_size;		//!< 書き込むデータのサイズ(32bit以下でbit単位で指定)
	unsigned int byte_ptr;	//!< バイト単位のリードポインタ
	unsigned int bit_ptr;	//!< byte_ptr内のビット位置を示すリードポインタ
} RUNLENGTH_PUT_BITS_PARAM;

/**
 * @brief dstへデータを書き出す
 * @param[in] put_bits_param ビット取得処理用パラメータ
 * @return RUNLENGTH_RET
 * @details srcからデータを読み出す
 */
static RUNLENGTH_RET put_bits(RUNLENGTH_PUT_BITS_PARAM* put_bits_param)
{
	RUNLENGTH_RET ret;
	unsigned int write_data;
	int write_byte;
	int remain_bits;
	int iter;

	write_data = (*(put_bits_param->dst+put_bits_param->byte_ptr) << 24) |
			(put_bits_param->put_data << (32-put_bits_param->put_size-put_bits_param->bit_ptr));
	write_byte = RUNLENGTH_MIN(4, (put_bits_param->put_size+put_bits_param->bit_ptr)/8);
	*(put_bits_param->dst + put_bits_param->byte_ptr) = (write_data >> 24) & 0xff;
	for (iter = 1; iter < write_byte; iter++) {
		*(put_bits_param->dst + put_bits_param->byte_ptr + iter) = (write_data >> (24 - iter*8)) & 0xff;
	}
	put_bits_param->byte_ptr += write_byte;

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

/**
 * @brief ランレングスエンコード
 * @param[in] enc_params エンコードパラメータ
 * @return int エンコード後のデータ長を返す @n
 *             エラー時は-1を返す
 * @details ランレングスエンコードを行う
 */
int runlength_encode(RUNLENGTH_ENC_PARAMS enc_params)
{
	unsigned int enc_unit;
	unsigned int enc_len_unit;
	int iter;
	int ret = 0;
	RUNLENGTH_PUT_BITS_PARAM put_bits_param = { 0 };

	if (enc_params.enc_unit <= 0) {
		enc_unit = RUNLENGTH_ENC_UNIT_DEFAULT;
	} else {
		enc_unit = enc_params.enc_unit;
	}
	if (enc_params.enc_len_unit <= 0) {
		enc_len_unit = RUNLENGTH_LEN_UNIT_DEFAULT;
	} else {
		enc_len_unit = enc_params.enc_len_unit;
	}

	if (enc_params.header == NULL) {
		put_bits_param.dst = enc_params.dst;
		put_bits_param.put_data = enc_unit;
		put_bits_param.put_size = 8;
		put_bits(&put_bits_param);
		ret += 1;
		
		put_bits_param.dst = enc_params.dst;
		put_bits_param.put_data = enc_len_unit;
		put_bits_param.put_size = 8;
		put_bits(&put_bits_param);
		ret += 1;

		put_bits_param.dst = enc_params.dst;
		put_bits_param.put_data = enc_params.src_len;
		put_bits_param.put_size = 32;
		put_bits(&put_bits_param);
		ret += 4;
	} else {
		enc_params.header[0] = enc_unit & 0xff;
		enc_params.header[1] = enc_len_unit & 0xff;
		for (iter = 0; iter < 4; iter++) {
			enc_params.header[iter+2] = ((unsigned int)(enc_params.src_len) >> (24 - iter*8)) & 0xff;
		}
	}

	return ret;
}

/**
 * @brief ランレングスデコード
 * @param[in] src デコード対象のデータ
 * @param[in] src_len デコード対象のデータ長
 * @param[out] dst デコード結果を格納するバッファ
 * @return int デコード後のデータ長を返す @n
 *             エラー時は-1を返す
 * @details ランレングスデコードを行う
 */
int runlength_decode(char* src, int src_len, char* dst)
{
	int ret = -1;

	return ret;
}

