# matplotlibを用いたグラフ描画のサンプル

## 概要

* 折れ線グラフ，棒グラフ，散布図，方対数グラフ(x軸，y軸)，両対数グラフを描画するサンプルプログラム
	* 折れ線グラフ

## 実行手順

	$ python3 matplotlib_sample.py --help
	$ python3 matplotlib_sample.py --graph_type line --output_dir out
	$ python3 matplotlib_sample.py --graph_type line --output_dir out --use_gui
	$ python3 matplotlib_sample.py --graph_type bar --output_dir out --use_gui
	$ python3 matplotlib_sample.py --graph_type mixed_line_bar --output_dir out --use_gui
	$ python3 matplotlib_sample.py --graph_type scatter --output_dir out --use_gui
	$ python3 matplotlib_sample.py --graph_type line,bar,mixed_line_bar,scatter --output_dir out --use_gui


