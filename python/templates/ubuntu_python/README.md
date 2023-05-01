# UbuntuベースのPython環境

UbuntuをベースとしたPython環境のテンプレート

## 使い方

### 前準備

```
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec --user $UID ubuntu_python bash
$ cd /work
```

### テストプログラムの実行

```
$ python3 ubuntu_python.py
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

