/**
 * @file main.c
 * @brief 探索プログラムのサンプル
 */

#include <string.h>
#include "search.h"
#include "quick_sort.h"
#include "common.h"

/**
 * @def SAMPLE_NUM
 * @brief 探索対象のデータ数
 */
#define SAMPLE_NUM	(10000)

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
 * @brief 探索対象データ生成関数
 * @param[in] num データ数
 * @param[in] seed 乱数シード
 * @param[out] dst 探索対象データを格納するバッファ
 * @return SEARCH_RET
 * @details 探索用データを生成する
 */
SEARCH_RET create_data(int num, int seed, int* dst)
{
	SEARCH_RET ret = SEARCH_RET_NOERROR;
	int i, j;
	int data_tmp;

	if (dst == NULL) {
		return SEARCH_RET_NULL;
	}

	srand(seed);
	for (i = 0; i < num; i++) {
		dst[i] = i;
	}

	for (i = 0; i < num; i++) {
		j = rand() % num;
		data_tmp = dst[i];
		dst[i] = dst[j];
		dst[j] = data_tmp;
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
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数 @n
 *            argv[1] : 結果出力ディレクトリ
 * @return int 0固定
 * @details 探索用データ生成及び各探索処理呼び出しと処理時間計測を行う
 */
int main(int argc, char* argv[])
{
	FILE* fp_data;
	FILE* fp_result;
	int data[SAMPLE_NUM];
	int sorted_data[SAMPLE_NUM];
	char* output_dir;
	char file_name[FILE_NAME_MAX];
	unsigned long addr_list[SAMPLE_NUM];
	int i;
	struct timespec tsStart, tsEnd, tsElapsedTime;

	if (argc != 2) {
		show_usage();
		exit(0);
	}
	output_dir = argv[1];

	sprintf(file_name, "%s/result.csv", output_dir);
	fp_result = fopen(file_name, "w");
	fprintf(fp_result, "探索アルゴリズム,処理時間[sec]\n");

	create_data(SAMPLE_NUM, RANDOM_SEED, data);
	sprintf(file_name, "%s/data.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,addr,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%p,%d\n", i, &data[i], data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}

	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	quick_sort(sorted_data, SAMPLE_NUM, NULL);
	sprintf(file_name, "%s/sorted_data.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "index,addr,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%d,%p,%d\n", i, &sorted_data[i], sorted_data[i]);
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}

	/* --- 線形探索 --- */
	clock_gettime(CLOCK_REALTIME, &tsStart);
	for (i = 0; i < SAMPLE_NUM; i++) {
		addr_list[i] = (unsigned long)linear_search(data, SAMPLE_NUM, i);
	}
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (linear_search) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "線形探索,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-linear_search.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "addr,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%p,%d\n", (int*)addr_list[i], *((int*)addr_list[i]));
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}

	/* --- 2分探索 --- */
	memcpy(sorted_data, data, SAMPLE_NUM * sizeof(int));
	clock_gettime(CLOCK_REALTIME, &tsStart);
	quick_sort(sorted_data, SAMPLE_NUM, NULL);
	for (i = 0; i < SAMPLE_NUM; i++) {
		addr_list[i] = (unsigned long)binary_search(sorted_data, SAMPLE_NUM, i);
	}
	clock_gettime(CLOCK_REALTIME, &tsEnd);
	tsElapsedTime.tv_sec = tsEnd.tv_sec - tsStart.tv_sec;
	tsElapsedTime.tv_nsec = tsEnd.tv_nsec - tsStart.tv_nsec;
	if (tsElapsedTime.tv_nsec < 0) {
		tsElapsedTime.tv_sec -= 1;
		tsElapsedTime.tv_nsec += 1000000000;
	}
	MY_PRINT(MY_PRINT_LVL_INFO, "elapsed time (binary_search) : %ld.%09ld[sec]\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);
	fprintf(fp_result, "2分探索,%ld.%09ld\n", tsElapsedTime.tv_sec, tsElapsedTime.tv_nsec);

	sprintf(file_name, "%s/result-binary_search.csv", output_dir);
	fp_data = fopen(file_name, "w");
	if (fp_data != NULL) {
		fprintf(fp_data, "addr,value\n");
		for (i = 0; i < SAMPLE_NUM; i++) {
			fprintf(fp_data, "%p,%d\n", (int*)addr_list[i], *((int*)addr_list[i]));
		}
		fclose(fp_data);
	} else {
		MY_PRINT(MY_PRINT_LVL_ERROR, "Cannot open file : %s\n", file_name);
		exit(0);
	}

	fclose(fp_result);
	return 0;
}

