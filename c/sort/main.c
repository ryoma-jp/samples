/**
 * @file main.c
 * @brief ソートプログラムのサンプル
 */

#include <stdlib.h>
#include <string.h>
#include <sort.h>
#include <common.h>

/**
 * @def SAMPLE_NUM
 * @brief ソート対象のデータ数
 */
#define SAMPLE_NUM	(100000)

/**
 * @def RANDOM_SEED
 * @brief 乱数シード @n
 *        処理の再現性を確保するために使用
 */
#define RANDOM_SEED	(1234)

/**
 * @def FILE_NAME_MAX
 * @brief ファイル名の最大文字数
 */
#define FILE_NAME_MAX	(1024)

/**
 * @brief ソート対象データ生成関数
 * @param[in] num データ数
 * @param[in] seed 乱数シード
 * @param[out] dst ソート対象データを格納するバッファ
 * @return SORT_RET
 * @details ソート用データを生成する
 */
SORT_RET create_data(int num, int seed, int* dst)
{
	SORT_RET ret = SORT_RET_NOERROR;
	int i;

	if (dst == NULL) {
		return SORT_RET_NULL;
	}

	srand(seed);
	for (i = 0; i < num; i++) {
		dst[i] = rand();
	}

	return ret;
}

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
int show_usage()
{
	printf("<< Usage >>\n");
	printf("  ./sort [output_dir]\n");
	printf("    output_dir : 結果出力ディレクトリ\n");

	return 0;
}

/**
 * @def TEST_SELECTION_SORT
 * @brief 選択法によるソート処理を実行する場合にセット
 */
#define TEST_SELECTION_SORT

/**
 * @def TEST_BUBBLE_SORT
 * @brief バブルソート処理を実行する場合にセット
 */
#define TEST_BUBBLE_SORT

/**
 * @def TEST_INSERT_SORT
 * @brief 挿入法によるソート処理を実行する場合にセット
 */
#define TEST_INSERT_SORT

/**
 * @def TEST_SHELL_SORT
 * @brief シェルソート処理を実行する場合にセット
 */
#define TEST_SHELL_SORT

/**
 * @def TEST_QUICK_SORT
 * @brief クイックソート処理を実行する場合にセット
 */
#define TEST_QUICK_SORT

/**
 * @def TEST_HEAP_SORT
 * @brief ヒープソート処理を実行する場合にセット
 */
#define TEST_HEAP_SORT

/**
 * @def TEST_MERGE_SORT
 * @brief マージソート処理を実行する場合にセット
 */
#define TEST_MERGE_SORT

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数 @n
 *                 argv[0] : 結果出力ディレクトリ
 * @return int 0固定
 * @details ソート用データを生成し，各ソート処理の呼び出し及び処理時間計測を行う @n
 *          引数で指定された結果出力ディレクトリに下記データを出力する
 *            - ソート対象データ : data.csv
 *            - 各ソートアルゴリズムの処理時間計測結果 : result.csv
 */
int main(int argc, char* argv[])
{
	FILE* fp_data;
	FILE* fp_result;
	int data[SAMPLE_NUM];
	int sorted_data[SAMPLE_NUM];
	char* output_dir;
	char file_name[FILE_NAME_MAX];
	int i;
	struct timespec tsStart, tsEnd, tsElapsedTime;

	if (argc != 2) {
		show_usage();
		exit(0);
	}
	output_dir = argv[1];

	sprintf(file_name, "%s/result.csv", output_dir);
	fp_result = fopen(file_name, "w");
	fprintf(fp_result, "ソートアルゴリズム,処理時間[sec]\n");

	/* --- 乱数データ生成 --- */
	create_data(SAMPLE_NUM, RANDOM_SEED, data);

	sprintf(file_name, "%s/data.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}

#ifdef TEST_SELECTION_SORT
	/* --- 選択法 --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	selection_sort(sorted_data, SAMPLE_NUM, NULL);
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (selection_sort) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "選択法,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-selection_sort.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}
#endif	/* --- TEST_SELECTION_SORT --- */

#ifdef TEST_BUBBLE_SORT
	/* --- バブルソート --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	bubble_sort(sorted_data, SAMPLE_NUM, NULL);
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (bubble_sort) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "バブルソート,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-bubble_sort.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}
#endif	/* --- TEST_BUBBLE_SORT --- */

#ifdef TEST_INSERT_SORT
	/* --- 挿入法 --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	insert_sort(sorted_data, SAMPLE_NUM, NULL);
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (insert_sort) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "挿入法,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-insert_sort.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}
#endif	/* --- TEST_INSERT_SORT --- */

#ifdef TEST_SHELL_SORT
	/* --- シェルソート --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	shell_sort(sorted_data, SAMPLE_NUM, NULL);
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (shell_sort) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "シェルソート,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-shell_sort.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}
#endif	/* --- TEST_SHELL_SORT --- */

#ifdef TEST_QUICK_SORT
	/* --- クイックソート --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	quick_sort(sorted_data, SAMPLE_NUM, NULL);
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (quick_sort) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "クイックソート,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-quick_sort.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}
#endif	/* --- TEST_QUICK_SORT --- */

#ifdef TEST_HEAP_SORT
	/* --- ヒープソート --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	heap_sort(sorted_data, SAMPLE_NUM, NULL);
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (heap_sort) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "ヒープソート,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-heap_sort.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}
#endif	/* --- TEST_HEAP_SORT --- */

#ifdef TEST_MERGE_SORT
	/* --- マージソート --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	merge_sort(sorted_data, SAMPLE_NUM, NULL);
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (merge_sort) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "マージソート,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-merge_sort.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%d\n", i, sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}
#endif	/* --- TEST_MERGE_SORT --- */

	fclose(fp_result);
	return 0;
}

