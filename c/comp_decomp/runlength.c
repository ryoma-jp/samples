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
 *     エンコード結果のヘッダにデコード後のデータサイズを格納しておく @n
 *     このパラメータはデコード時，ファイル終端の端数を判断する用途でも使用する @n
 *     - 端数 @n
 *       圧縮単位16byte，データサイズ24byteのように，エンコード対象のデータサイズが圧縮単位となる保証がなく，端数が生じる @n
 *       端数に対して0を埋めてエンコードし，デコード時はヘッダに格納されたデコード後のデータサイズを見てゼロ埋めしたデータ数を判断する @n
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
 * @brief ランレングスエンコード処理のコア部分
 * @param[in] enc_params エンコードパラメータ
 * @param[in] get_bits_param エンコード対象のデータのアドレス設定済みの取得パラメータ
 * @param[in,out] put_bits_param エンコード結果を格納するアドレス設定済みの書き出しパラメータ @n
 *                               put_bits_param.dstにエンコード結果を格納する
 * @return int エンコード後のデータ長を返す @n
 *             エラー時は-1を返す
 * @details ランレングスエンコードを行う
 */
static int runlength_encode_core(RUNLENGTH_ENC_PARAMS enc_params, 
					GET_BITS_PARAM get_bits_param,
					PUT_BITS_PARAM put_bits_param)
{
	int ret = 0;
	int remain = enc_params.src_len * 8;
	int enc_len_unit;
	long enc_bit = 0;
	unsigned int enc_unit_data;
	unsigned int enc_unit_data_next;

	get_bits_param.read_size = enc_params.enc_unit;
	while (remain >= enc_params.enc_unit) {
		get_bits(&get_bits_param, GET_BITS_FALSE);
		remain -= enc_params.enc_unit;
		enc_unit_data = get_bits_param.read_data;
		enc_len_unit = 1;

		if (remain >= enc_params.enc_unit) {
			get_bits(&get_bits_param, GET_BITS_TRUE);
			enc_unit_data_next = get_bits_param.read_data;
			while (enc_unit_data == enc_unit_data_next) {
				get_bits(&get_bits_param, GET_BITS_FALSE);
				remain -= enc_params.enc_unit;
				enc_len_unit += 1;

				if (remain >= enc_params.enc_unit) {
					get_bits(&get_bits_param, GET_BITS_TRUE);
					enc_unit_data_next = get_bits_param.read_data;
				} else {
					break;
				}
			}
		}

		put_bits_param.put_data = enc_unit_data;
		put_bits_param.put_size = enc_params.enc_unit;
		put_bits(&put_bits_param);

		put_bits_param.put_data = enc_len_unit;
		put_bits_param.put_size = enc_params.enc_len_unit;
		put_bits(&put_bits_param);

		enc_bit += enc_params.enc_unit + enc_params.enc_len_unit;
	}

	if (remain > 0) {
		get_bits_param.read_size = remain;
		get_bits(&get_bits_param, GET_BITS_FALSE);
		enc_unit_data = get_bits_param.read_data << (8 - (remain % 8));
		enc_len_unit = 1;

		put_bits_param.put_data = enc_unit_data;
		put_bits_param.put_size = enc_params.enc_unit;
		put_bits(&put_bits_param);

		put_bits_param.put_data = enc_len_unit;
		put_bits_param.put_size = enc_params.enc_len_unit;
		put_bits(&put_bits_param);

		enc_bit += enc_params.enc_unit + enc_params.enc_len_unit;
	}

	ret = enc_bit / 8;
	if (enc_bit % 8 > 0) {
		ret += 1;
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
	int iter;
	int ret = 0;
	PUT_BITS_PARAM put_bits_param = { 0 };
	GET_BITS_PARAM get_bits_param = { 0 };

	if (enc_params.enc_unit <= 0) {
		enc_params.enc_unit = RUNLENGTH_ENC_UNIT_DEFAULT;
	} 
	if (enc_params.enc_len_unit <= 0) {
		enc_params.enc_len_unit = RUNLENGTH_LEN_UNIT_DEFAULT;
	}

	if (enc_params.header == NULL) {
		put_bits_param.dst = enc_params.dst;
		put_bits_param.put_data = enc_params.enc_unit;
		put_bits_param.put_size = 8;
		put_bits(&put_bits_param);
		ret += 1;
		
		put_bits_param.dst = enc_params.dst;
		put_bits_param.put_data = enc_params.enc_len_unit;
		put_bits_param.put_size = 8;
		put_bits(&put_bits_param);
		ret += 1;

		put_bits_param.dst = enc_params.dst;
		put_bits_param.put_data = enc_params.src_len;
		put_bits_param.put_size = 32;
		put_bits(&put_bits_param);
		ret += 4;
	} else {
		enc_params.header[0] = enc_params.enc_unit & 0xff;
		enc_params.header[1] = enc_params.enc_len_unit & 0xff;
		for (iter = 0; iter < 4; iter++) {
			enc_params.header[iter+2] = ((unsigned int)(enc_params.src_len) >> (24 - iter*8)) & 0xff;
		}
	}

	get_bits_param.src = enc_params.src;
	ret += runlength_encode_core(enc_params, get_bits_param, put_bits_param);

	return ret;
}

/**
 * @brief ランレングスデコード処理のコア部分
 * @param[in] dec_params デコードパラメータ
 * @param[in] get_bits_param デコード対象のデータのアドレス設定済みの取得パラメータ
 * @param[in,out] put_bits_param デコード結果を格納するアドレス設定済みの書き出しパラメータ @n
 *                               put_bits_param.dstにデコード結果を格納する
 * @return int デコード後のデータ長を返す @n
 *             エラー時は-1を返す
 * @details ランレングスデコードを行う
 */
static int runlength_decode_core(RUNLENGTH_DEC_PARAMS dec_params, 
					GET_BITS_PARAM get_bits_param,
					PUT_BITS_PARAM put_bits_param,
					int enc_unit, int enc_len_unit, unsigned int dst_size)
{
	unsigned int enc_data;
	int enc_len;
	int iter;

	while (put_bits_param.byte_ptr < dst_size) {
		get_bits_param.read_size = enc_unit;
		get_bits(&get_bits_param, GET_BITS_FALSE);
		enc_data = get_bits_param.read_data;
	
		get_bits_param.read_size = enc_len_unit;
		get_bits(&get_bits_param, GET_BITS_FALSE);
		enc_len = get_bits_param.read_data;
	
		put_bits_param.put_data = enc_data;
		put_bits_param.put_size = enc_unit;
		for (iter = 0; iter < enc_len; iter++) {
			put_bits(&put_bits_param);
		}
	}

	return put_bits_param.byte_ptr;
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
int runlength_decode(RUNLENGTH_DEC_PARAMS dec_params)
{
	unsigned int dst_size = 0;
	int enc_unit = 0;
	int enc_len_unit = 0;
	int iter;
	int ret = 0;
	PUT_BITS_PARAM put_bits_param = { 0 };
	GET_BITS_PARAM get_bits_param = { 0 };

	if (dec_params.header == NULL) {
		get_bits_param.src = dec_params.src;
		get_bits_param.read_size = 8;
		get_bits(&get_bits_param, GET_BITS_FALSE);
		enc_unit = get_bits_param.read_data;
		
		get_bits_param.read_size = 8;
		get_bits(&get_bits_param, GET_BITS_FALSE);
		enc_len_unit = get_bits_param.read_data;

		get_bits_param.read_size = 32;
		get_bits(&get_bits_param, GET_BITS_FALSE);
		dst_size = get_bits_param.read_data;
	} else {
		enc_unit = dec_params.header[0];
		enc_len_unit = dec_params.header[1];
		for (iter = 0; iter < 4; iter++) {
			dst_size = (dst_size << 8) | dec_params.header[iter+2];
		}
	}

	put_bits_param.dst = dec_params.dst;
	ret = runlength_decode_core(dec_params, get_bits_param, put_bits_param,
			enc_unit, enc_len_unit, dst_size);

	return ret;
}

