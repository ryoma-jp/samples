# argparseモジュールのテスト

## 概要

* argparseモジュールを用いた引数入力のサンプル  
* argparse.ArgumentParser()でプログラムの概要を記述  
	* formatter_classにargparse.RawTextHelpFormatterを指定すると，helpに改行を用いることができる  
* add_argument()関数で引数を追加  
	* 第一引数で引数名を指定  
	* destで引数値を格納する変数名を指定  
	* typeで引数の型を指定  
	* requiredで引数指定が必須か否かを指定 … True：必須，False：任意  
	* helpで引数の説明を記述  
	* bool型は，typeで指定するのではなく，actionで指定する  
'store_true'で引数指定された場合にTrueが格納，'store_false'で引数指定された場合にFalseが格納される  
* parser.parse_args()関数で引数解析を実行  

## 実行手順

	$ python3 argparse_sample.py --help
	$ python3 argparse_sample.py --string sample --int 100 --float 10.12098 --bool


