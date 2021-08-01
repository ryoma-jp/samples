#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
import cv2
import numpy as np
import struct

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='画像データをbyteデータへ変換するツール',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--input_img', dest='input_img', type=str, default=None, required=True, \
            help='入力画像')
    parser.add_argument('--output_file', dest='output_file', type=str, default=None, required=True, \
            help='出力ファイル')
    parser.add_argument('--output_fmt', dest='output_fmt', type=str, default='BGR', required=False, \
            help='出力時のカラーフォーマット(Grayscale, BGR, RGB)')

    args = parser.parse_args()

    return args

def img2byte(input_img, output_file, output_fmt='BGR'):
    # --- 入力画像読み込み ---
    img = cv2.imread(input_img)
    img_shape = img.shape
    if (output_fmt == 'RGB'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        # --- BGRとグレースケールはフォーマット変換しない ---
        pass
    img = img.reshape([-1])

    # --- byteデータへ変換 ---
    try:
        bytefile = open(output_file, 'wb')
    except:
        print('[ERROR] Open outout file is failed: {}'.format(output_file))
        exit(-1)

    # --- ヘッダパラメータ: ../../data_loader.c ---
    n_data = len(img) + 16      # データサイズにヘッダ(4パラメータ，16byte分)を加算
    pack_data = struct.pack('<i', n_data)
    bytefile.write(pack_data)

    d_type = 0
    pack_data = struct.pack('<i', d_type)
    bytefile.write(pack_data)

    for data_header in img_shape:   # height, width, channel
        pack_data = struct.pack('<i', data_header)
        bytefile.write(pack_data)
    d_type = 0
    pack_data = struct.pack('<i', d_type)
    bytefile.write(pack_data)

    for pixel_data in img:
        pack_data = struct.pack('<B', pixel_data)
        bytefile.write(pack_data)

    return

def main():
    # --- 引数処理 ---
    args = ArgParser()
    print('args.input_img : {}'.format(args.input_img))
    print('args.output_file : {}'.format(args.output_file))
    print('args.ouptut_fmt : {}'.format(args.output_fmt))

    img2byte(args.input_img, args.output_file, output_fmt=args.output_fmt)

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


