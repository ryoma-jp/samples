
#ifndef __RUNLENGTH_H__
#define __RUNLENGTH_H__

/**
 * @def RUNLENGTH_ENC_UNIT_DEFAULT
 * @brief 圧縮単位のデフォルト値(ビット数)
 */
#define RUNLENGTH_ENC_UNIT_DEFAULT	(8)

/**
 * @def RUNLEHGTH_LEN_UNIT_DEFAULT
 * @brief 連長桁のデフォルト値(ビット数)
 */
#define RUNLENGTH_LEN_UNIT_DEFAULT	(8)

/**
 * @def RUNLENGTH_HEADER_LEN
 * @brief ヘッダ長(バイト数)
 */
#define RUNLENGTH_HEADER_LEN	(2)

/**
 * @struct _RUNLENGTH_ENC_PARAMS
 * @brief ランレングスエンコードのパラメータ
 */
typedef struct _RUNLENGTH_ENC_PARAMS {
	char* src;		//!< エンコード対象のデータ
	int src_len;		//!< エンコード対象のデータ長[byte単位]
	int enc_unit;		//!< エンコード単位[bit単位]．0以下の指定はデフォルト値を使用する．
	int enc_len_unit;	//!< 連長桁[bit単位]．0以下の指定はデフォルト値を使用する．
	char* dst;		//!< エンコード結果を格納するバッファ
	char* header;		//!< ヘッダを格納するバッファ．NULL指定でヘッダをdstに埋め込む．
} RUNLENGTH_ENC_PARAMS;

/**
 * @struct _RUNLENGTH_DEC_PARAMS
 * @brief ランレングスデコードのパラメータ
 */
typedef struct _RUNLENGTH_DEC_PARAMS {
	char* src;		//!< デコード対象のデータ
	int src_len;		//!< デコード対象のデータ長[byte単位]
	char* dst;		//!< デコード結果を格納するバッファ
	char* header;		//!< ヘッダが格納されているバッファ．NULL指定でヘッダをdstから読み込む．
} RUNLENGTH_DEC_PARAMS;

/**
 * @enum _RUNLENGTH_RET
 * @brief ランレングスエンコード・デコード処理の戻り値
 */
typedef enum _RUNLENGTH_RET {
	RUNLENGTH_RET_NOERROR,	//!< エラーなし
} RUNLENGTH_RET;

extern int runlength_encode(RUNLENGTH_ENC_PARAMS enc_params);
extern int runlength_decode(RUNLENGTH_DEC_PARAMS dec_params);

#endif /*__RUNLENGTH_H__ */
