#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
from calc_lib import *

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='パッケージ配布のサンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()

	# --- calc_lib呼び出し ---
	print(add(13, 17))
	print(sub(13, 17))
	print(mul(13, 17))
	print(dev(13, 17))

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()


