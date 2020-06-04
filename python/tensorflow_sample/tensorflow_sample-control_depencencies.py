#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
import tensorflow as tf

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='TensorFlowの実装サンプル(tf.control_dependencies)', 
				formatter_class=argparse.RawTextHelpFormatter)

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()

	# --- case1 ---
	#  * sess.run([upd1, upd2])と書くと，upd1とupd2の計算が非同期で実施され，
	#    v1とv2の更新タイミング不定により計算結果も不定になる
	print('[case1]')
	v1 = tf.Variable(0)
	v2 = tf.Variable(0)
	upd1 = tf.assign(v1, v2 + 1)
	upd2 = tf.assign(v2, v1 + 1)
	init = tf.global_variables_initializer()

	for i in range(10):
		with tf.compat.v1.Session() as sess:
			sess.run(init)
			sess.run([upd1, upd2])
			print(sess.run([v1, v2]))

	sess.close()
	
	# --- case2 ---
	#  * tf.control_depencenciesを用いることで，withブロック内のコンテキスト実行前に
	#    new_v1, new_v2が処理されるため，計算結果を固定化できる
	print('[case2]')
	v1 = tf.Variable(0)
	v2 = tf.Variable(0)
	new_v1 = v2 + 1
	new_v2 = v1 + 1
	with tf.control_dependencies([new_v1, new_v2]):
		upd1 = tf.assign(v1, new_v1)
		upd2 = tf.assign(v2, new_v2)
	init = tf.global_variables_initializer()

	for i in range(10):
		with tf.compat.v1.Session() as sess:
			sess.run(init)
			sess.run([upd1, upd2])
			print(sess.run([v1, v2]))

	sess.close()
	
	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()


