#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
from data_loader import cifar10
from calc_distance import euclidean_dist

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='データ間の距離計算処理のサンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--dist_type', dest='dist_type', type=str, default='EUCLIDEAN', required=False, \
			help='距離種別(EUCLIDEAN, or ...(T.B.D)')
	parser.add_argument('--data_type', dest='data_type', type=str, default='CIFAR-10', required=False, \
			help='データ種別(CIFAR-10, or ...(T.B.D)')
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print('[INFO] args.dist_type: {}'.format(args.dist_type))
	print('[INFO] args.data_type: {}'.format(args.data_type))
	print('[INFO] args.dataset_dir: {}'.format(args.dataset_dir))
	
	if (args.data_type == "CIFAR-10"):
		train_images, train_labels, test_images, test_labels = cifar10.load_cifar10(args.dataset_dir)
		
	if (args.dist_type == "EUCLIDEAN"):
		data_dist = euclidean_dist.euclidean_dist(train_images[0], train_images[1])
	else:
		print('[ERROR] Unknown dist_type: {}'.format(args.dist_type))
		quit()
	
	print('[RESULT] data distance: {}'.format(data_dist))

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

