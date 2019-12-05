/**
 * @file huffman.c
 * @brief ハフマンデコード・エンコード
 *   - データの出現頻度をもとに圧縮する方法
 *   - データの出現頻度の高いデータに短いビット列を割り当て，データの出現頻度の低いデータに長いビット列を割り当てる
 *   - 符号化時にハフマン木を作成する
 *   - エンコード結果のヘッダにハフマン木を保存しておき，デコード時に読み出せるように実装する
 *   - エンコードしたデータのデコード結果を格納するバッファサイズを決めるために， @n
 *     エンコード結果のヘッダにデコード後のデータサイズを格納しておく @n
 */

#include <string.h>
#include "huffman.h"
#include "common.h"

/**
 * @brief クイックソートのサブルーチン
 * @param[in,out] data ソート範囲 @n
 *                     ソート結果を上書き更新する
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @return HUFFMAN_RET
 * @details クイックソートによるソート処理のサブルーチン @n
 *          再帰的処理による分割処理
 */
static HUFFMAN_RET quick_sort_sub(int* data, int key_num)
{
	HUFFMAN_RET ret = HUFFMAN_RET_NOERROR;
	int pivot = data[key_num-1];
	int left_ptr = 0;
	int right_ptr = key_num-1;
	int data_tmp;

	while (left_ptr < right_ptr) {
		while ((data[left_ptr] > pivot)) {
			left_ptr += 1;
		}
		while ((pivot >= data[right_ptr]) && (left_ptr < right_ptr)) {
			right_ptr -= 1;
		}

		if (left_ptr < right_ptr) {
			data_tmp = data[left_ptr];
			data[left_ptr] = data[right_ptr];
			data[right_ptr] = data_tmp;
		}
	}
	data[key_num-1] = data[left_ptr];
	data[left_ptr] = pivot;

	if (left_ptr > 1) {
		quick_sort_sub(data, left_ptr);
	}
	if (key_num - (right_ptr+1) > 1) {
		quick_sort_sub(&data[right_ptr+1], key_num - (right_ptr+1));
	}

	return ret;
}

/**
 * @brief クイックソート
 * @param[in] src ソート範囲
 * @param[in] key_num ソート範囲のサイズ(キー数)
 * @param[out] dst ソート結果を格納するバッファのアドレス @n
 *                 NULLの場合はsrcの配列をソート結果で上書きする
 * @return HUFFMAN_RET
 * @details クイックソートによるソート処理
 */
static HUFFMAN_RET quick_sort(int* src, int key_num, int* dst)
{
	HUFFMAN_RET ret = HUFFMAN_RET_NOERROR;

	if (dst == NULL) {
		dst = src;
	} else {
		memcpy(dst, src, key_num * sizeof(int));
	}

	quick_sort_sub(dst, key_num);

	return ret;
}

/**
 * @brief 線形探索
 * @param[in] keys 探索範囲
 * @param[in] key_num 探索範囲のサイズ(キー数)
 * @param[in] search_key 探索対象のキー
 * @return int* 探索対象キーが格納されているアドレス(=探索結果)
 *              探索対象キーが見つからない場合はNULLを返す
 * @details 線形探索を行う
 */
static int* linear_search(int* keys, int key_num, int search_key)
{
	/* --- 変数宣言 --- */
	int* ret = NULL;
	int i;

	/* --- 探索 --- */
	for (i = 0; i < key_num; i++) {
		if (keys[i] == search_key) {
			ret = &keys[i];
			break;
		}
	}

	return ret;
}

/**
 * @brief ハフマン木の作成
 * @param[in] src 入力データ
 * @param[in] src_len 入力データ長[byte]
 * @param[in/out] tree tree->enc_unitに従ってハフマン木を生成しtree.listに格納する @n
 *                     tree->listにはNULLを指定して関数コールする
 * @return HUFFMAN_RET 処理結果
 * @details ハフマン木を作成する @n
 *          ハフマン木の削除(メモリ解放)はdelete_huffman_tree()をコールする
 */
static HUFFMAN_RET create_huffman_tree(char* src, int src_len, HUFFMAN_TREE* tree)
{
	HUFFMAN_RET ret = HUFFMAN_RET_NOERROR;
	GET_BITS_PARAM get_bits_param = { 0 };
	int code_num = 1 << tree->enc_unit;
	int code_count[code_num];
	int code_count_sorted[code_num];
	struct {
		int code;
		int count;
	} code_list[code_num];
	int* code_addr;
	int pre_code;
	int same_code_count;
	int iter;

	get_bits_param.src = src;
	get_bits_param.read_size = tree->enc_unit;

	for (iter = 0; iter < code_num; iter++) {
		code_count[iter] = 0;
	}

	while (get_bits_param.byte_ptr < src_len) {
		get_bits(&get_bits_param, GET_BITS_FALSE);
		code_count[get_bits_param.read_data] += 1;
	}

	quick_sort(code_count, code_num, code_count_sorted);

	printf("<< code_count >>\n");
	for (iter = 0; iter < code_num; iter++) {
		printf("  [%03d] %d\n", iter, code_count[iter]);
	}
	printf("<< code_count_sorted>>\n");
	for (iter = 0; iter < code_num; iter++) {
		printf("  [%03d] %d\n", iter, code_count_sorted[iter]);
	}

	iter = 0;
	printf("<< code_list >>\n");
	while ((iter < code_num) && (code_count_sorted[iter] > 0)) {
		code_addr = linear_search(code_count, code_num, code_count_sorted[iter]);
		if (iter > 0) {
			pre_code = code_list[iter-1].code;
			code_addr = linear_search(code_count, code_num, code_count_sorted[iter]);

			same_code_count = 0;
			if (pre_code == code_addr-code_count) {
				while (code_count_sorted[iter] == code_count_sorted[iter+same_code_count]) {
					code_addr = linear_search(code_addr+1, code_num-(code_count-code_addr)-1, code_count_sorted[iter+same_code_count]);
					code_list[iter+same_code_count].code = (int)(code_addr-code_count);
					code_list[iter+same_code_count].count = code_count_sorted[iter+same_code_count];
					printf("  *code_list[%d] : %d, %d\n", iter+same_code_count, code_list[iter+same_code_count].code, code_list[iter+same_code_count].count);

					same_code_count += 1;
				}
				iter += same_code_count;
			} else {
				code_list[iter].code = (int)(code_addr-code_count);
				code_list[iter].count = code_count_sorted[iter];
				printf("  code_list[%d] : %d, %d\n", iter, code_list[iter].code, code_list[iter].count);

				iter += 1;
			}
		} else {
			code_list[iter].code = (int)(code_addr-code_count);
			code_list[iter].count = code_count_sorted[iter];
			printf("  code_list[%d] : %d, %d\n", iter, code_list[iter].code, code_list[iter].count);

			iter += 1;
		}
	}

	return ret;
}

/**
 * @brief ハフマン木の削除
 * @param[in] tree 削除するハフマン木
 * @return HUFFMAN_RET 処理結果
 * @details ハフマン木を削除する
 */
static HUFFMAN_RET delete_huffman_tree(HUFFMAN_TREE tree)
{
	HUFFMAN_RET ret = HUFFMAN_RET_NOERROR;

	return ret;
}

/**
 * @brief ハフマンエンコード
 * @param[in] enc_params エンコードパラメータ
 * @param[out] dst エンコード結果を格納するバッファ
 * @return int エンコード後のデータ長を返す @n
 *             エラー時は-1を返す
 * @details ハフマンエンコードを行う
 */
int huffman_encode(HUFFMAN_ENC_PARAMS enc_params)
{
	int ret = -1;
	HUFFMAN_TREE huffman_tree = { 0 };

	huffman_tree.enc_unit = enc_params.enc_unit;
	create_huffman_tree(enc_params.src, enc_params.src_len, &huffman_tree);

	delete_huffman_tree(huffman_tree);

	return ret;
}

/**
 * @brief ハフマンデコード
 * @param[in] dec_params デコードパラメータ
 * @param[out] dst デコード結果を格納するバッファ
 * @return int デコード後のデータ長を返す @n
 *             エラー時は-1を返す
 * @details ハフマンデコードを行う
 */
int huffman_decode(HUFFMAN_DEC_PARAMS dec_params)
{
	int ret = -1;

	return ret;
}

