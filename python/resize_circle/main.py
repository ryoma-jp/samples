#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import io
import pandas as pd
import argparse
from resize_circle import resize_circle

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='Pythonモジュールごとの画像ダウンサンプリング',
				formatter_class=argparse.RawTextHelpFormatter)


	args = parser.parse_args()

	return args

def main():
	# --- 円のリサイズ ---
	rc = resize_circle.ResizeCircle()
	rc.resize_opencv()
	rc.resize_pil()

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()


