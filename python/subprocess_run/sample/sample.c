/*******************************************************
 * [ 説明 ]
 *   Pythonのsubprocess.runの動作確認用のサンプルコード
 *******************************************************/

/*******************************************************
 * インクルードファイル
 *******************************************************/
#include <sample.h>
#include <sample_common.h>

/*******************************************************
 * 定数定義
 *******************************************************/

/*******************************************************
 * 列挙体／構造体
 *******************************************************/

/*******************************************************
 * 関数宣言
 *******************************************************/

/*******************************************************
 * 変数宣言
 *******************************************************/

/*******************************************************
 * [ 関数名 ]
 *   main
 * [ 説明 ]
 *   メイン関数
 *   テンプレートでは"Hello World!"の表示のみ
 *
 * [ 引数 ]
 *   なし
 *
 * [ 戻り値 ]
 *   1234固定
 *
 *******************************************************/
int main(int argc, char* argv[])
{
	MY_PRINT(MY_PRINT_LVL_INFO, "Hello World!\n");

//	return 1234;
	return 34;	/* subprocess.runの戻り値は255まで？ */
}

