/**
 * @file main.c
 * @brief 処理時間計測のサンプル
 */
#include <measuring_proc_time.h>
#include <common.h>
#include <time.h>

/**
 * @def CNT_MAX
 * @brief 計測する処理のループカウンタ
 */
#define CNT_MAX		(1600000000)

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details clock()とclock_gettime()での処理時間計測処理を実装
 */
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

