#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import titanic
from tabnet.tabnet import TabNet

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
	parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=True, \
			help='結果を出力するディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print(args.dataset_dir)
	print(args.output_dir)
	
	os.makedirs(args.output_dir, exist_ok=True)
	
	# --- データセット読み込み ---
	train_data, train_labels, test_data = titanic.load_titanic(args.dataset_dir)
	print(train_data)
	print(test_data)
	
	x_train = train_data.drop(labels=["PassengerId", "Survived", "Name"], axis=1, inplace=False)
	y_train = train_labels
	x_train_columns = x_train.columns
	
	x_train = np.array(x_train.values, dtype=np.float64)
	y_train = np.array(y_train.values, dtype=np.float64)
	
	# --- TabNet学習 ---
	tn_clf = TabNet()
	scores, feature_importances = tn_clf.fit(x_train, y_train)
	
	print(feature_importances)
	
	# --- 特徴の重要度を出力 ---
	plt.figure()
	plt.barh(x_train_columns, feature_importances.mean(axis=0))
	plt.title('feature_importance')
	plt.tight_layout()
	plt.savefig(os.path.join(args.output_dir, 'feature_importance.png'))
	plt.close()
	
	# --- Kaggle submission用のcsvを出力 ---
	x_test = test_data.drop(labels=["PassengerId", "Name"], axis=1, inplace=False)
	x_test = np.array(x_test.values, dtype=np.float64)
	prediction = tn_clf.inference(x_test)
	print(prediction.shape)
	print(prediction)
	print(np.round(prediction.mean(axis=0)).astype(int))
	
	df_submission = pd.DataFrame({
						"PassengerId": test_data["PassengerId"],
						"Survived": np.round(prediction.mean(axis=0)).astype(int)})
	df_submission.to_csv(os.path.join(args.output_dir, 'submission.csv'), index=False)
	
	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

