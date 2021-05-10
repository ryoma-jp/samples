#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import titanic, sarcos
from tabnet.tabnet import TabNet

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='TabNetの学習サンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--dataset_type', dest='dataset_type', type=str, default=None, required=True, \
			help='データセット種別(Titanic, SARCOS, or ...(T.B.D)')
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットディレクトリ')
	parser.add_argument('--tabnet_type', dest='tabnet_type', type=str, default=None, required=False, \
			help='TabNet種別(TabNet-S, or ...(T.B.D))')
	parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=True, \
			help='結果を出力するディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print(args.dataset_type)
	print(args.dataset_dir)
	print(args.tabnet_type)
	print(args.output_dir)
	
	os.makedirs(args.output_dir, exist_ok=True)
	
	# --- データセット読み込み ---
	if (args.dataset_type == 'Titanic'):
		train_data, train_labels, test_data = titanic.load_titanic(args.dataset_dir)
		print(train_data)
		print(test_data)
		
		x_train = train_data.drop(labels=["PassengerId", "Survived", "Name"], axis=1, inplace=False)
		y_train = train_labels
		x_train_columns = x_train.columns
		
		x_train = np.array(x_train.values, dtype=np.float64)
		y_train = np.array(y_train.values, dtype=np.float64)
		
		kf_splits = 5
	elif (args.dataset_type == 'SARCOS'):
		x_train, y_train, x_test, y_test = sarcos.load_sarcos(args.dataset_dir)
		print(x_train.shape)
		print(y_train.shape)
		print(x_test.shape)
		print(y_test.shape)
		
		kf_splits = 10
	else:
		print('[ERROR] Unknown dataset_type: {}'.format(args.dataset_type))
		quit()
	
	# --- TabNet学習 ---
	tn_model = TabNet()
	scores, feature_importances = tn_model.fit(x_train, y_train, kf_splits=kf_splits, tabnet_type=args.tabnet_type)
	
	print(feature_importances)
	
	# --- 特徴の重要度を出力 ---
	if (args.dataset_type == 'Titanic'):
		plt.figure()
		plt.barh(x_train_columns, feature_importances.mean(axis=0))
		plt.title('feature_importance')
		plt.tight_layout()
		plt.savefig(os.path.join(args.output_dir, 'feature_importance.png'))
		plt.close()
		
	# --- テストデータの推論結果を出力 ---
	if (args.dataset_type == 'Titanic'):
		# --- Kaggle submission用のcsvを出力 ---
		x_test = test_data.drop(labels=["PassengerId", "Name"], axis=1, inplace=False)
		x_test = np.array(x_test.values, dtype=np.float64)
		prediction = tn_model.inference(x_test)
		print(prediction.shape)
		print(prediction)
		print(np.round(prediction.mean(axis=0)).astype(int))
		
		df_submission = pd.DataFrame({
							"PassengerId": test_data["PassengerId"],
							"Survived": np.round(prediction.mean(axis=0)).astype(int)})
		df_submission.to_csv(os.path.join(args.output_dir, 'submission.csv'), index=False)
	elif (args.dataset_type == 'SARCOS'):
		prediction = tn_model.inference(x_test)
		print(prediction.shape)
		print(prediction)
		
		squared_error = np.linalg.norm((prediction[0:len(x_test)] - y_test), axis=1)
		print(squared_error.shape)
		mse = squared_error.mean()
		print(mse)
	else:
		print('[ERROR] Unknown dataset_type: {}'.format(args.dataset_type))
		quit()
	
	
	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

