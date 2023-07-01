# ChatGPTのプログラミング能力を試す

ChatGPTにいくつかの方法でプログラムの出力を指示し，プログラミング能力を試した  
今回のお題はソートで仕様を与えて出力させたり，Python言語からC言語に変換させたが，欠陥なく出力された  
ソートというお題そのものが簡単すぎたこともあるかもしれないが，それでも動作するプログラムが自動的に出力されるのは，すごいなぁと改めて感じた

## テーマ：ソート

10万レコードを昇順で並べ替える関数をChatGPTに出力させる  
出力する言語はC++とする  
ChatGPTへ指示する方法は下記の3種である

試験1. 並べ替えの要件を日本語で与え，ソートを行う関数を出力するように指示する  
試験2. Python言語でsortingモジュールを使用しない関数を，C言語に変換するように指示する  
試験3. Python言語でsortingモジュールを使用する関数を，C言語に変換するように指示する  

* 仕様
  * 1から10万の整数値が整数型で格納された領域のアドレスを引数にとる
  * 昇順に並べ替えた結果が格納された領域のアドレスを返す

### 試験1　プロンプトプログラミング

#### プロンプト

```
数値を昇順に並べ替えるプログラムをC言語で作成してください
仕様は以下の通りです

- 1から10万の整数値が整数型で格納された領域のアドレスを引数にとる
- 昇順に並べ替えた結果が格納された領域のアドレスを返す
```

#### ChatGPTの出力結果

```
#include <stdio.h>

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
    int arr[100000];  // 配列の宣言

    // 配列に1から10万の整数値を格納する
    for (int i = 0; i < 100000; i++) {
        arr[i] = i + 1;
    }

    // 数値を昇順に並べ替える
    sortAscending(arr, 100000);

    // 結果の表示（最初の10個の要素のみ表示）
    for (int i = 0; i < 10; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}

```

### 試験2　Python→C++変換(sortingモジュールを使用しない)

#### プロンプト

```
以下のPythonプログラムをC言語に変換してください

def sort(data):
    """sort
    
    sort function
    
    Args:
        data: list of integer values
    
    Returns:
        sorted values
    """
    
    if (len(data) <= 1):
        return data
    
    pivot = data.pop(0)
    left = [i for i in data if i <= pivot]
    right = [i for i in data if i > pivot]
    
    left = sort(left)
    right = sort(right)
    
    return left + [pivot] + right
```

#### ChatGPTが出力したプログラム

```
#include <stdio.h>
#include <stdlib.h>

void sort(int *data, int length);

void merge(int *data, int *left, int left_length, int *right, int right_length);

void printArray(int *data, int length);

int main() {
    int data[] = {5, 3, 8, 4, 2, 7, 1, 6};
    int length = sizeof(data) / sizeof(data[0]);

    sort(data, length);

    printf("Sorted array: ");
    printArray(data, length);

    return 0;
}

void sort(int *data, int length) {
    if (length <= 1) {
        return;
    }

    int pivot = data[0];
    int *left = malloc((length - 1) * sizeof(int));
    int *right = malloc((length - 1) * sizeof(int));
    int left_length = 0;
    int right_length = 0;

    for (int i = 1; i < length; i++) {
        if (data[i] <= pivot) {
            left[left_length] = data[i];
            left_length++;
        } else {
            right[right_length] = data[i];
            right_length++;
        }
    }

    sort(left, left_length);
    sort(right, right_length);
    merge(data, left, left_length, right, right_length);

    free(left);
    free(right);
}

void merge(int *data, int *left, int left_length, int *right, int right_length) {
    int i = 0;
    int j = 0;
    int k = 0;

    while (i < left_length && j < right_length) {
        if (left[i] <= right[j]) {
            data[k] = left[i];
            i++;
        } else {
            data[k] = right[j];
            j++;
        }
        k++;
    }

    while (i < left_length) {
        data[k] = left[i];
        i++;
        k++;
    }

    while (j < right_length) {
        data[k] = right[j];
        j++;
        k++;
    }
}

void printArray(int *data, int length) {
    for (int i = 0; i < length; i++) {
        printf("%d ", data[i]);
    }
    printf("\n");
}
```


### 試験3　Python→C++変換(sortingモジュールを使用する)

#### プロンプト

```
以下のPythonのプログラムをC言語に変換してください

def sort(data):
    """sort
    
    sort function
    
    Args:
        data: list of integer values
    
    Returns:
        sorted values
    """
    
    ret = sorting.quick(data)
    
    return ret
```

#### ChatGPTが出力したプログラム

```c
#include <stdio.h>

void quickSort(int arr[], int low, int high);

void sort(int data[], int size) {
    quickSort(data, 0, size - 1);
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;

    return (i + 1);
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int main() {
    int data[] = {5, 8, 2, 4, 1};
    int size = sizeof(data) / sizeof(data[0]);

    sort(data, size);

    printf("Sorted values: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", data[i]);
    }

    return 0;
}

```

### 前準備

```
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec --user $UID ubuntu_python bash
$ cd /work
```

### プログラムの実行

#### 試験1

```
$ test1.sh
```

#### 試験2

```
$ test2.sh
```

#### 試験3

```
$ test3.sh
```

### ドキュメントの作成 ([Sphinx](https://www.sphinx-doc.org))

#### プロジェクトの作成

```
$ sphinx-quickstart docs
Welcome to the Sphinx 7.0.0 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: docs

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

The project name will occur in several places in the built documentation.
> Project name: Develop environment for Python
> Author name(s): Ryoichi MATSUMOTO
> Project release []:

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
> Project language [en]:

Creating file /work/docs/source/conf.py.
Creating file /work/docs/source/index.rst.
Creating file /work/docs/Makefile.
Creating file /work/docs/make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file /work/docs/source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
```

#### configの更新

``docs/source/conf.py``を編集してドキュメント化対象のPythonファイルのパスを設定と拡張機能の追加を行う．

``sphinx.ext.autodoc``はdocstringの自動読み込み，``sphinx.ext.napoleon``はスタイルをパースする拡張機能である．

```
$ diff -up docs/source/conf.py.org docs/source/conf.py
--- docs/source/conf.py.org     2023-05-02 07:58:53.154436448 +0900
+++ docs/source/conf.py 2023-05-02 08:32:08.594436316 +0900
@@ -3,6 +3,10 @@
 # For the full list of built-in configuration values, see the documentation:
 # https://www.sphinx-doc.org/en/master/usage/configuration.html

+import os
+import sys
+sys.path.insert(0, os.path.abspath('../../'))
+
 # -- Project information -----------------------------------------------------
 # https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

@@ -13,7 +17,7 @@ author = 'Ryoichi MATSUMOTO'
 # -- General configuration ---------------------------------------------------
 # https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

-extensions = []
+extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

 templates_path = ['_templates']
 exclude_patterns = []
```


#### rstファイルの生成

ドキュメント化対象ファイルの``rst``ファイルを生成する．

```
$ sphinx-apidoc -f -o ./docs/source/ .
```

#### ドキュメント化対象ファイルをindexへ追加

ドキュメント化対象(生成したrstファイル)を``index.rst``へ追加する．

```
$ diff -up docs/source/index.rst.org docs/source/index.rst
--- docs/source/index.rst.org   2023-05-02 08:39:11.284436729 +0900
+++ docs/source/index.rst       2023-05-02 08:33:57.354439062 +0900
@@ -10,6 +10,8 @@ Welcome to Develop environment for Pytho
    :maxdepth: 2
    :caption: Contents:

+   modules
+   ubuntu_python
```


#### ドキュメントをビルド(HTML)

ドキュメントをビルドし，HTMLファイルを生成する．  
``docs/build/html/index.html``がトップページである．

```
$ sphinx-build -b html docs/source/ docs/build/html
```

## 参考

* [とほほのPython入門 - Sphinx](https://www.tohoho-web.com/python/sphinx.html)

