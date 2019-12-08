
#ifndef __HUFFMAN_H__
#define __HUFFMAN_H__

/**
 * @def HUFFMAN_ENC_UNIT_DEFAULT
 * @brief 圧縮単位のデフォルト値(ビット数)
 */
#define HUFFMAN_ENC_UNIT_DEFAULT	(8)

/**
 * @struct _HUFFMAN_TREE_LIST
 * @brief ハフマン木をリスト構造で表現する @n
 *        リストを線形探索しながらdataにヒットすれば0を付与，@n
 *        ヒットしなければ1を付与してrightを判定する @n
 */
typedef struct _HUFFMAN_TREE_LIST {
	unsigned int data;	//!< エンコード対象のデータ
//	struct _HUFFMAN_TREE_LIST* left;	//!< ハフマン木の左枝
	struct _HUFFMAN_TREE_LIST* right;	//!< ハフマン木の右枝
} HUFFMAN_TREE_LIST;

/**
 * @struct _HUFFMAN_TREE
 * @brief ハフマン符号化時に生成するハフマン木
 */
typedef struct _HUFFMAN_TREE {
	int enc_unit;			//!< エンコード単位
	HUFFMAN_TREE_LIST* list;	//!< ハフマン木の本体
} HUFFMAN_TREE;

/**
 * @struct _HUFFMAN_ENC_PARAMS
 * @brief ハフマンエンコードのパラメータ
 */
typedef struct _HUFFMAN_ENC_PARAMS {
	char* src;		//!< エンコード対象のデータ
	int src_len;		//!< エンコード対象のデータ長[byte]
	int enc_unit;		//!< エンコード単位[bit単位]．0以下の指定はデフォルト値を使用する．
	char* dst;		//!< エンコード結果を格納するバッファ
	char* header;		//!< ヘッダを格納するバッファ．NULL指定でヘッダをdstに埋め込む．
} HUFFMAN_ENC_PARAMS;

/**
 * @struct _HUFFMAN_DEC_PARAMS
 * @brief ハフマンデコードのパラメータ
 */
typedef struct _HUFFMAN_DEC_PARAMS {
	char* src;		//!< デコード対象のデータ
	int src_len;		//!< デコード対象のデータ長[byte単位]
	char* dst;		//!< デコード結果を格納するバッファ
	char* header;		//!< ヘッダが格納されているバッファ．NULL指定でヘッダをdstから読み込む．
} HUFFMAN_DEC_PARAMS;

/**
 * @enum _HUFFMAN_RET
 * @brief ハフマンエンコード・デコード処理の戻り値
 */
typedef enum _HUFFMAN_RET {
	HUFFMAN_RET_NOERROR,	//!< エラーなし
} HUFFMAN_RET;

extern int huffman_encode(HUFFMAN_ENC_PARAMS enc_params);
extern int huffman_decode(HUFFMAN_DEC_PARAMS dec_params);

#endif /*__HUFFMAN_H__ */

