# 信号処理　フィルタ（LPF, HPF）のサンプル

## 概要

* LPF, HPFのサンプル  
* 乱数10000サンプルを，サンプリングレート10kHz　1秒の信号として，フィルタ処理を実行

## 実行手順

### Jupyter Notebook

	docker_run.shで起動後，
		http://localhost:10000
	へブラウザでアクセスし，コンソールに表示されるトークン部分をコピペしてログインする

### コマンドライン

	$ python3 filter.py --help
	$ python3 filter.py

## 参考

* https://watlab-blog.com/2019/04/30/scipy-lowpass/
* https://detail-infomation.com/filter-cutoff-cutoff-frequency/
* https://detail-infomation.com/filter-cutoff-frequency-3db/
* https://www.electronics-tutorials.ws/filter/filter_2.html

