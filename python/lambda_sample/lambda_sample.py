#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='無名関数lambdaの利用サンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	args = parser.parse_args()

	return args

def add(x1, x2):
	return x1+x2

def main():
	# --- 引数処理 ---
	args = ArgParser()

	# --- Function ---
	print(add(7, 11))
	lambda_add = lambda x1, x2: x1+x2
	print(lambda_add(7, 11))
	print(add(7, 11) == lambda_add(7, 11))

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()


