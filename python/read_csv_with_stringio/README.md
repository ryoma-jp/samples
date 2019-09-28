# io.StringIOモジュールでカンマ区切りの文字列をread_csvで読み込む

## 概要

* read_csv()の引数に，io.StringIO(<文字列>)を指定する
* read_csv()の引数に，skipinitialspace=True を指定すると，各文字列先頭のスペースを削除できる
* 読み込んだ結果は，out.csv として出力する
* to_csv()の引数に，header=False を指定すると，ヘッダなしでcsv出力できる
* to_csv()の引数に，index=False を指定すると，インデックスなしでcsv出力できる

## 実行手順

	$ python3 read_csv_with_stringio.py


