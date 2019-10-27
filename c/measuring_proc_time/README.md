# 処理時間計測のサンプル

## 概要

* 処理時間計測方法として，clock()とclock_gettime()を紹介  
	* clock()はPOSIX環境，Windows環境の両方で利用できる  
	* clock_gettime()はPOSIX環境でのみ利用できる
* Windows環境で利用できるAPIとしてGetSystemTime()もあるらしいが保留

## 実行手順

	$ make
	$ ./measuring_proc_time

# 参考

* https://www.mm2d.net/main/prog/c/time-05.html

