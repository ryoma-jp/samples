#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse
from data_loader import common

_data_type = os.environ['DATA_TYPE']
if (_data_type == 'CIFAR-10'):
	from data_loader import cifar10
elif (_data_type == 'Titanic'):
	from data_loader import titanic
elif (_data_type == 'SARCOS'):
	from data_loader import sarcos
elif (_data_type == 'COCO2014'):
	from data_loader import coco_loader
elif (_data_type == 'MoviePoster'):
	from data_loader import movie_poster
elif (_data_type == 'MNIST'):
	from data_loader import mnist
else:
	print('[ERROR] Unknown DATA_TYPE({})'.format(_data_type))
	quit()

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
			help='データ種別(CIFAR-10, Titanic, SARCOS, COCO2014, MoviePoster, MNIST or ...(T.B.D)')
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
		train_images, train_labels, test_images, test_labels = cifar10.load_cifar10(args.dataset_dir, img_dir='./cifar10_images')
		print(train_images.shape)
		print(train_labels.shape)
		print(test_images.shape)
		print(test_labels.shape)
		
		label_index = common.get_label_index(train_labels)
		print(label_index.shape)
		for _label_index in label_index:
			print(train_labels[_label_index].argmax(axis=1).min(), train_labels[_label_index].argmax(axis=1).max())
	elif (args.data_type == "Titanic"):
		train_data, train_labels, test_data = titanic.load_titanic(args.dataset_dir)
		print(train_data.shape)
		print(train_labels.shape)
		print(test_data.shape)
	elif (args.data_type == "SARCOS"):
		train_data, train_labels, test_data, test_labels = sarcos.load_sarcos(args.dataset_dir)
		print(train_data.shape)
		print(train_labels.shape)
		print(test_data.shape)
		print(test_labels.shape)
	elif (args.data_type == "COCO2014"):
		ann_types = ['captions', 'instances', 'person_keypoints']
		for ann_type in ann_types:
			print('[INFO] ann_type: {}'.format(ann_type))
			train_data, train_labels, validation_data, validation_labels, test_data = coco_loader.load_coco2014(args.dataset_dir, ann_type=ann_type)
			print(train_data.shape)
			print(train_labels)
			print(validation_data.shape)
			print(validation_labels)
			print(test_data.shape)
	elif (args.data_type == "MoviePoster"):
		train_images, train_labels, test_images, test_labels = movie_poster.load_movie_poster(args.dataset_dir, output_dir='./output/movie_poster', random_seed=0)
		print(train_images.shape)
		print(train_labels.shape)
		print(test_images.shape)
		print(test_labels.shape)
		
	elif (args.data_type == "MNIST"):
		train_images, train_labels, test_images, test_labels = mnist.load_mnist(args.dataset_dir)
		print(train_images.shape)
		print(train_labels.shape)
		print(test_images.shape)
		print(test_labels.shape)
		
		df_train = common.save_image_files(train_images, train_labels, os.path.join(args.dataset_dir, 'train_images'), img_shape=(28, 28))
		df_test = common.save_image_files(test_images, test_labels, os.path.join(args.dataset_dir, 'test_images'), img_shape=(28, 28))
		
	else:
		print('[ERROR] Unknown data_type: {}'.format(args.data_type))
		quit()
	
	# --- JSON形式での保存 ---
	json_params = {
		'samples': df_train['file'],
		'labels': train_labels,
		'onehot': True,
		'name': 'train_dataset',
		'save_dir': os.path.join(args.dataset_dir, 'train_images'),
		'task': 'image_classification',
	}
	common.convert_json(json_params)
	
	json_params = {
		'samples': df_test['file'],
		'labels': test_labels,
		'onehot': True,
		'name': 'test_dataset',
		'save_dir': os.path.join(args.dataset_dir, 'test_images'),
		'task': 'image_classification',
	}
	common.convert_json(json_params)
	
	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

