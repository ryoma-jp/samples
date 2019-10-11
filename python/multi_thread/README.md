# マルチスレッドプログラムのサンプル

## 概要

* 複数スレッドを作成して，各スレッドから10秒をカウントする外部プログラム(counter.py)を起動する  
* counter.pyは10秒のカウント中に出力するログの出力間隔を指定可能で，各スレッドで指定間隔を変える  
* counter.pyの呼び出しは，引数--use_subprocessでsubprocessモジュールを使用するか関数コールとするかを選択する  

## 実行手順

	$ python3 multi_thread.py --n_thread 3
	$ python3 multi_thread.py --n_thread 3 --use_subprocess

## 制約事項

* --use_subprocess有効時は，teeコマンドでcounter.py標準エラー出力を画面とファイルの両方に出力するので，bashのみ動作する

## 参考

* https://qiita.com/castaneai/items/9cc33817419896667f34
* https://qiita.com/tag1216/items/db5adcf1ddcb67cfefc8

