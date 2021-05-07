#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
from data_loader import titanic
from tabnet.tabnet import TabNet

import numpy as np
#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='Titanicデータセットを用いたTabNetのサンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print(args.dataset_dir)
	
	train_data, train_labels, test_data = titanic.load_titanic(args.dataset_dir)
	print(train_data)
	print(test_data)
	
	x_train = train_data.drop(labels=["PassengerId", "Survived", "Name"], axis=1, inplace=False)
	y_train = train_labels
	
	x_train = np.array(x_train.values, dtype=np.float64)
	y_train = np.array(y_train.values, dtype=np.float64)
	
	tn_clf = TabNet()
	tn_clf.fit(x_train, y_train)

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

