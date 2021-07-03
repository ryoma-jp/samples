#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import io
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='metricsログをグラフに統合するツール',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--metrics_list', dest='metrics_list', type=str, default=None, required=True, \
			help='metricsを記述したcsvファイル(カンマ区切りで指定)')
	parser.add_argument('--metrics_names', dest='metrics_names', type=str, default=None, required=True, \
			help='metrics_listで指定するmetrics名のリスト(カンマ区切りで指定)')
	parser.add_argument('--output_dir', dest='output_dir', type=str, default='./output', required=False, \
			help='グラフ出力先のディレクトリを指定')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print('[INFO] Arguments')
	print('  * args.metrics_list = {}'.format(args.metrics_list))
	print('  * args.metrics_names = {}'.format(args.metrics_names))
	print('  * args.output_dir = {}'.format(args.output_dir))
	
	# --- 出力ディレクトリ作成 ---
	os.makedirs(args.output_dir, exist_ok=True)
	
	# --- metricsファイルを取得 ---
	metrics_list = pd.read_csv(io.StringIO(args.metrics_list), header=None, skipinitialspace=True).values[0]
	
	# --- metrix名を取得 ---
	metrics_name = pd.read_csv(io.StringIO(args.metrics_names), header=None, skipinitialspace=True).values[0]

	# --- metricsグラフ作成 ---
	for i, metrics_file in enumerate(metrics_list):
		df_metrics = pd.read_csv(metrics_file)
		
		if (i == 0):
			dict_metrics = {}
			for metrics in df_metrics.columns.values[1:]:
				dict_metrics[metrics] = pd.DataFrame(df_metrics['epoch'])
		
		for metrics in df_metrics.columns.values[1:]:
			dict_metrics[metrics] = dict_metrics[metrics].assign(temp_item=df_metrics[metrics])
			dict_metrics[metrics] = dict_metrics[metrics].rename(columns={'temp_item': metrics_name[i]})
	
	for key in dict_metrics.keys():
		dict_metrics[key].to_csv(os.path.join(args.output_dir, '{}.csv'.format(key)), index=False)
		
		plt.figure()
		for column in dict_metrics[key].columns.values[1:]:
			plt.plot(dict_metrics[key]['epoch'], dict_metrics[key][column], label=column)
		plt.xlabel('epoch')
		plt.ylabel(key)
		plt.legend()
		plt.tight_layout()
		plt.savefig(os.path.join(args.output_dir, '{}.png'.format(key)))
		plt.close()
	
	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

