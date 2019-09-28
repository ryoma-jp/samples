# 外部プログラムの実行サンプル

## 概要

* 外部プログラムを実行するサンプルプログラム
* subprocess.run()関数で実行できる
	* stdout, stderrにsubprocess.PIPEを指定すると子プロセス間で入出力を行う
	* subprocess.runの戻り値に外部プログラムの戻り値や標準出力等を格納できる
* os.system()関数でも同様の処理ができるが，非推奨らしい

## 実行手順

	$ python3 subprocess_run.py --help
	$ python3 subprocess_run.py --bin 'ls -al'

	$ cd ./sample
	$ make
	$ cd ..
	$ python3 subprocess_run.py --bin sample/sample


## 参照

* https://maku77.github.io/python/env/call-external-program.html
* https://kakurasan.blogspot.com/2017/03/python-run-external-process.html

