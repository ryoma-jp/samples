#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
from data_loader import cifar10

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='データセット読み込み処理のサンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--data_type', dest='data_type', type=str, default='CIFAR-10', required=False, \
			help='データ種別(CIFAR-10, or ...(T.B.D)')
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print(args.data_type)
	print(args.dataset_dir)
	
	if (args.data_type == "CIFAR-10"):
		train_images, train_labels, test_images, test_labels = cifar10.load_cifar10(args.dataset_dir)
		print(train_images.shape)
		print(train_labels.shape)
		print(test_images.shape)
		print(test_labels.shape)
		

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

