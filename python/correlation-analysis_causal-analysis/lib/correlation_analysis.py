#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import numpy as np

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数 : ピアソンの積率相関係数
# [Input]
#   * x: 独立変数(ndarray)
#   * y: 従属変数(ndarray)
# [Output]
#   * r: ピアソンの積率相関係数
# [T.B.D]
#   * 多次元のデータ間の相関が計算できるように拡張したい
#---------------------------------
def peason(x, y):
	x_err = x - x.mean()
	y_err = y - y.mean()
	
	r = np.dot(x_err, y_err) / np.sqrt(np.sum(x_err ** 2) * np.sum(y_err ** 2))
	return r

#---------------------------------
# 関数 : スピアマンの順位相関係数
# [Input]
#   * x: 独立変数(ndarray)
#   * y: 従属変数(ndarray)
# [Output]
#   * rho: スピアマンの順位相関係数
#---------------------------------
def spearman(x, y):
	n = len(x)
	rho = 1 - (6 * np.sum((x-y)**2)) / (n * (n+1) * (n-1))
	return rho

#---------------------------------
# 関数 : メイン関数(ライブラリのテスト用)
#---------------------------------
def main():
	import argparse
	
	def _argparse():
		parser = argparse.ArgumentParser(description='相関分析モジュールのテスト',
					formatter_class=argparse.RawTextHelpFormatter)

		# --- 引数を追加 ---
		#  [T.B.D]

		args = parser.parse_args()

		return args
	
	# --- 引数処理 ---
	args = _argparse()
	print('[INFO] Arguments')
	print('  * T.B.D')
	
	# --- データを乱数で生成(1D) ---
	rng = np.random.default_rng(seed=1234)
	x = rng.random(3)
	y = rng.random(3)
	print("[Peason (1D input)]")
	print("  * np.corrcoef = {}".format(np.corrcoef(x, y)))
	print("  * peason = {}".format(peason(x, y)))
	
	# --- データを乱数で生成(2D) ---
	rng = np.random.default_rng(seed=1234)
	x = rng.random([3, 3])
	y = rng.random([3, 3])
	corrcoef = np.corrcoef(x, y, rowvar=True)
	print("[Peason (2D input)]")
	print("  * np.corrcoef = {}".format(corrcoef))
	print("  * np.corrcoef.shape = {}".format(corrcoef.shape))
	
	print("  * peason = {}".format([peason(x[0], x[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(x[1], x[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(x[2], x[i]) for i in range(3)]))
	
	print("  * peason = {}".format([peason(x[0], y[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(x[1], y[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(x[2], y[i]) for i in range(3)]))
	
	print("  * peason = {}".format([peason(y[0], x[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(y[1], x[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(y[2], x[i]) for i in range(3)]))
	
	print("  * peason = {}".format([peason(y[0], y[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(y[1], y[i]) for i in range(3)]))
	print("  * peason = {}".format([peason(y[2], y[i]) for i in range(3)]))
	
	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

