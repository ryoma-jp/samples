/**
 * @file main.c
 * @brief C言語ソースコードのテンプレート
 */

#include <template.h>
#include <common.h>

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
int show_usage()
{
	printf("<< Usage >>\n");
	printf("  ./template\n");

	return 0;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details テンプレートでは"Hello World!"の表示のみを行う
 */
int main(int argc, char* argv[])
{
	show_usage();
	template_print();

	return 0;
}

