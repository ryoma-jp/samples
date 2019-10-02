#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import glob
import argparse
import tqdm
import re

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='globモジュールを用いてファイル探索するサンプルプログラム',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--search_dir', dest='search_dir', type=str, default=None, required=False, \
            help='探索対象のディレクトリ')
    parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=False, \
            help='探索結果(テキストファイル)を出力するディレクトリ')

    args = parser.parse_args()

    return args

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    # --- 数値でsplit ---
    parts = numbers.split(value)
    
    # --- split後はparts[1], parts[3], ... が数値になるのでintにキャスト ---
    parts[1::2] = map(int, parts[1::2])
    
    return parts

def main():

    # --- 引数処理 ---
    args = ArgParser()

    # --- ファイル探索 ---
    file_list = glob.glob(os.path.join(args.search_dir, 'sample_file_*.bin'))
    file_list_with_sorted = sorted(glob.glob(os.path.join(args.search_dir, 'sample_file_*.bin')))
    file_list_with_getmtime_sort = sorted(glob.glob(os.path.join(args.search_dir, 'sample_file_*.bin')), key=numericalSort)
    file_list_with_sub_dir = sorted(glob.glob(os.path.join(args.search_dir, '**', 'sample_file_*.bin'), recursive=True), key=numericalSort)

    # --- 探索結果を保存 ---
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, 'file_list.txt'), 'w') as f:
        for _file in tqdm.tqdm(file_list):
            f.write('{}\n'.format(_file))
    with open(os.path.join(args.output_dir, 'file_list_with_sorted.txt'), 'w') as f:
        for _file in tqdm.tqdm(file_list_with_sorted):
            f.write('{}\n'.format(_file))
    with open(os.path.join(args.output_dir, 'file_list_with_numerical_sort.txt'), 'w') as f:
        for _file in tqdm.tqdm(file_list_with_getmtime_sort):
            f.write('{}\n'.format(_file))
    with open(os.path.join(args.output_dir, 'file_list_with_sub_dir.txt'), 'w') as f:
        for _file in tqdm.tqdm(file_list_with_sub_dir):
            f.write('{}\n'.format(_file))

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()

