#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import sys
import argparse
import logging
import numpy as np
import tensorflow as tf

import tensorflow_datasets as tfds

#---------------------------------
# 環境設定
#---------------------------------

# --- ログ ---
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%dT%H:%M:%S")
handler.setFormatter(fmt)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG)

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='画像データをダウンロードする',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--dataset', dest='dataset', type=str, default='imagenet_v2', required=False, \
            help='イメージ画像を選択(cifar10, mnist, imagenet_v2 等)'
                 '※https://www.tensorflow.org/datasets/catalog/overview#image_classification から選択')
    parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default='download', required=False, \
            help='データセット保存先のディレクトリを指定')
    parser.add_argument('--image_dir', dest='image_dir', type=str, default='images', required=False, \
            help='画像保存先のディレクトリを指定')

    args = parser.parse_args()

    return args

def main():
    # --- 引数処理 ---
    args = ArgParser()
    logger.info('<< arguments >>')
    logger.info('--------------------------------------')
    logger.info(f'args.dataset : {args.dataset}')
    logger.info(f'args.dataset_dir : {args.dataset_dir}')
    logger.info(f'args.image_dir : {args.image_dir}')
    logger.info('--------------------------------------')
    
    # --- データダウンロード ---
    ds, info = tfds.load(args.dataset, split='test', shuffle_files=True, with_info=True, data_dir=args.dataset_dir)
    logger.info('<< ds >>')
    logger.info(ds)
    logger.info('<< info >>')
    logger.info(info)
    
    # --- データ処理 ---
    n_ds = len(ds)
    for i, ds_ in enumerate(ds):
        if (i % (n_ds // 10) == 0):
            logger.info(f'[Progress] {i} / {n_ds}')
        
        im, name = ds_['image'], ds_['image/file_name']
        logger.debug(tf.get_static_value(name).decode())
        logger.debug(tf.get_static_value(im))
        
        name = tf.get_static_value(name).decode()   # tf.Tensor() -> String
        tf.io.write_file(
            os.path.join(args.image_dir, name),
            tf.image.encode_jpeg(im))
        
    logger.info(f'[Progress] {i+1} / {n_ds} (DONE)')
    
    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()

