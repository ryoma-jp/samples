#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import sys
import struct
import numpy as np
import pandas as pd
import argparse

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='float32データをbyteデータに変換するサンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()

	# --- byteデータに変換するfloatデータを生成 ---
	np.random.seed(1234)
	float_data = np.random.rand(5, 5, 3)
#	print(float_data)
	print('data_num = {}'.format(len(float_data.reshape([-1]))))
	print(float_data.reshape([-1]))
	float_data = float_data.reshape([-1])

#	print(type(sys.float_info.max))
#	print(struct.pack('<d', sys.float_info.max))

	with open('output.bin', 'ab') as f:
		for _float_data in float_data:
			pack_data = struct.pack('<f', _float_data)
			f.write(pack_data)

#	f_tmp = 0.1
#	f_tmp_pack = struct.pack('<f', f_tmp)
#
#	print(type(f_tmp))
#	print(f_tmp_pack)
#	print(struct.unpack('<f', f_tmp_pack))
#
#	with open('f_tmp.bin', 'wb') as f:
#		f.write(f_tmp_pack)


	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()


