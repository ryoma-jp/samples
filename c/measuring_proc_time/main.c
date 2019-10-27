/*******************************************************
 * [ 説明 ]
 *   処理時間計測のサンプル
 *******************************************************/

/*******************************************************
 * インクルードファイル
 *******************************************************/
#include <measuring_proc_time.h>
#include <common.h>
#include <time.h>

/*******************************************************
 * 定数定義
 *******************************************************/
#define CNT_MAX		(1600000000)

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
 *
 * [ 引数 ]
 *   なし
 *
 * [ 戻り値 ]
 *   0固定
 *
 *******************************************************/
int main(int argc, char* argv[])
{
	clock_t clStart, clEnd;
	struct timespec tsStart, tsEnd, tsElapsedTime;
	int i;

	clStart = clock();
	for (i = 0; i < CNT_MAX; i++) ;
	clEnd = clock();
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (clock) : %.2f[sec]\n", (double)(clEnd-clStart)/CLOCKS_PER_SEC);

	clock_gettime(CLOCK_REALTIME, &tsStart);
	for (i = 0; i < CNT_MAX; i++) ;
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (clock_gettime) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	return 0;
}

