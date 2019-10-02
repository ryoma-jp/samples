# 独自モジュールをimportするサンプル

## 概要

* 下記のディレクトリ構成で，modulesを共通モジュールとしtool1, tool2, ... などから呼び出すケースを想定  
		./
		  ├ modules/
		  │   ├ SubModule1/
		  │   │   └ SubModule1.py
		  │   └ SubModule2/
		  │       └ SubModule2.py
		  ├ tool1/
		  │   └ main.py
		  └ tool2/
		       └ main.py
* tool1, tool2からはmodulesが見えるように，sys.pathにmodulesへのパス追加が必要  
* modulesへのパス追加は絶対パスを追加する  
Pythonでは，pythonコマンドを実行したディレクトリがルートとなる仕様なので，例えば，tool1以下でmain.pyをコールすると相対パスでは上位ディレクトリが見えず，importできない  
main.pyが格納されているディレクトリの絶対パスに対してmodulesを指すようにパスを追加すればこの問題を解決できる  
* 共通モジュールをパッケージ化してPython環境にインストールするという方法もある  
→ https://github.com/ryoma-jp/libs/tree/master/python/dist_sample

## 実行手順

	$ python3 tool1/main.py
	$ python3 tool2/main.py

