# 配布用パッケージ作成サンプル

## 概要

* 配布用パッケージ作成サンプル  
* cython_c_in_tempは古いAPIで最新では使用されていないので，cythonizeで生成されるCコードはpyxと同じディレクトリとなる  
Cython/Distutils/old_build_ext.py  
* ルートディレクトリを汚さないように，dist/以下にpyxの一時コピーを作成する(src_tmp)  

## 実行手順

	$ cd dist
	$ ./dist.sh
	$ ./test.sh


