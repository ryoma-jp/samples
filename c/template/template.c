/**
 * @file template.c
 * @brief C言語ソースコードのテンプレート
 */

#include <template.h>
#include <common.h>

/**
 * @brief "Hello World!"を表示する関数
 * @return int 0固定
 * @details テンプレートでは"Hello World!"の表示のみを行う
 */
int template_print()
{
	MY_PRINT(MY_PRINT_LVL_INFO, "Hello World!\n");

	return 0;
}

