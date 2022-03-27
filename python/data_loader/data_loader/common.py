#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import cv2
import json
import tqdm
import numpy as np
import pandas as pd

def get_label_index(label, onehot=True):
	"""get_label_index
	ラベルインデックスを取得する
	"""
	if (onehot):
		label = np.argmax(label, axis=1)
	n_category = max(label)+1
	
	return np.array([np.arange(len(label))[label==i] for i in range(n_category)])

def save_image_files(images, labels, output_dir, img_shape=None):
	"""save_image_files
	画像データファイルを生成する
	<output_dir>/imagesに画像ファイルを保存する
	<output_dir>直下にIDとファイル名を紐づけるjsonファイルを保存する
	
	Args:
		images: 読み込んだデータセット(ndarray)
		labels: 正解ラベル(ndarray)
		output_dir: 画像データを出力するディレクトリ
		img_size: 画像サイズ．Noneの場合はimagesのshapeを画像サイズとする．
	"""
	
	# --- 画像保存ディレクトリを生成 ---
	image_dir = os.path.join(output_dir, 'images')
	os.makedirs(image_dir, exist_ok=True)
	
	# --- 各画像データを保存する ---
	dict_image_file = {
		'id': [],
		'file': [],
		'class_id': [],
	}
	for i, (image, label) in enumerate(tqdm.tqdm(zip(images, labels), total=min(len(images), len(labels)))):
		image_file = os.path.join('images', f'{i:08}.png')
		
		if (img_shape is not None):
			image = image.reshape(img_shape)
		cv2.imwrite(os.path.join(output_dir, image_file), image)
		
		dict_image_file['id'].append(i)
		dict_image_file['file'].append(image_file)
		dict_image_file['class_id'].append(int(np.argmax(label)))
	
	# --- jsonファイル保存 ---
	with open(os.path.join(output_dir, 'info.json'), 'w') as f:
		json.dump(dict_image_file, f, ensure_ascii=False, indent=4)
	
	# --- jsonファイル情報をpandasで読み込んで返す ---
	df_info = pd.read_json(json.dumps(dict_image_file))
	
	return df_info

def convert_json(json_params):
	"""convert_json
	データセットをjson形式で保存する
	json形式は，データセットの情報を保存するテキストとデータファイル群のセットである
	
	Args:
		json_params: データセット情報を辞書型で指定する
			'samples': データセットの入力ファイルリスト
			'labels': データセットの正解ラベルリスト
			'onehot': 正解ラベルリストのonehot表現のフラグ(True: onehot, False: 非onehot)
			'name': データセット名
			'save_dir': 保存先のディレクトリパス
			'task': データセット種別('image_classification')
	"""
	
	# --- データセットディレクトリの作成 ---
	os.makedirs(json_params['save_dir'], exist_ok=True)
	
	# --- jsonファイルに保存する基本情報をセット ---
	dict_json = {
		'name': json_params['name'],
		'root_dir': os.path.abspath(json_params['save_dir']),
		'task': json_params['task'],
		'metadata': [],
	}
	
	# --- metadata生成 ---
	metadata = []
	for i, (sample, label) in enumerate(tqdm.tqdm(zip(json_params['samples'], json_params['labels']),
								total=min(len(json_params['samples']), len(json_params['labels'])))):
		if (json_params['onehot']):
			label = int(np.argmax(label))
		dict_meta = {
			'id': i,
			'file_path': sample,
			'annotation': {
				'class_id': label,
				'class_name': label,
			},
		}
		
		metadata.append(dict_meta)
	dict_json['metadata'] = metadata
	
	# --- jsonファイルの保存 ---
	with open(os.path.join(json_params['save_dir'], 'dataset.json'), 'w') as f:
		json.dump(dict_json, f, ensure_ascii=False, indent=4)
	
	return
	