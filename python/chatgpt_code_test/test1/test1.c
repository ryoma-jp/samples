#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CSV_LINE_MAX (1048576)
#define CSV_MAX_ROW (1)
#define CSV_MAX_COL (100000)

// 配列の要素を交換する関数
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 数値を昇順に並べ替える関数
void sortAscending(int *arr, int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
            }
        }
    }
}

int main() {
    FILE* file;
    char csv_line[CSV_LINE_MAX];
    int csv_data[CSV_MAX_ROW][CSV_MAX_COL];
    int row = 0;
    int col = 0;
	int i, j;
    
    // load data
    file = fopen("data/data.csv", "r");
    while (fgets(csv_line, sizeof(csv_line), file)) {
        char* token = strtok(csv_line, ",");
        while (token != NULL) {
            csv_data[row][col] = atoi(token);
            col++;
            token = strtok(NULL, ",");
        }
        col = 0;
        row++;
    }
    fclose(file);
    
    // 数値を昇順に並べ替える
    sortAscending(csv_data[0], 100000);

    // ソート後のデータを出力
    file = fopen("./test1/test1_result_c.txt", "w");
    for (i = 0; i < CSV_MAX_COL; i++) {
        fprintf(file, "%d\n", csv_data[0][i]);
    }
    fclose(file);

    return 0;
}
