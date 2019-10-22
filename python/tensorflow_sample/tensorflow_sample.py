#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
import numpy as np
import tensorflow as tf

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='TensorFlowの実装サンプル\n'
                ' * 行列計算はnumpyと計算結果を比較するように実装する\n'
                ' * 気が向いたら学習サンプルも実装する',
                formatter_class=argparse.RawTextHelpFormatter)

    args = parser.parse_args()

    return args

class CalcMatrix():
    def __init__(self):
        return

    def show(self):
        print('<< Calc Matrix>>')
        # --- 加算・減算 ---
        print('mat1 + mat2 = {}'.format(self.add))
        print('mat1 - mat2 = {}'.format(self.sub))

        # --- 積(アダマール積) ---
        print('mat1 * mat2 = {}'.format(self.mul))

        # --- 転置 ---
        print('mat2.transpose(0, 2, 1) = {}'.format(self.transpose))

        # --- 内積1 : dot ---
        print('dot(mat1, mat2.transpose(0, 2, 1)) = {}'.format(self.dot))
        print('dot.shape = {}'.format(self.dot.shape))

        # --- 内積2 : matmul ---
        print('matmul(mat1, mat2.transpose(0, 2, 1)) = {}'.format(self.matmul))
        print('matmul.shape = {}'.format(self.matmul.shape))

        # --- 行列式 ---
        print('det(np.matmul(mat1, mat2)) = {}'.format(self.det))
        print('det.shape = {}'.format(self.det.shape))

        # --- 逆行列 ---
        print('inv(np.matmul(mat1, mat2)) = {}'.format(self.inv))
        print('inv.shape = {}'.format(self.inv.shape))

        # --- 三角関数 ---
        print('sin(mat1) = {}'.format(self.sin))
        print('cos(mat1) = {}'.format(self.cos))
        print('tan(mat1) = {}'.format(self.tan))

        return

class CalcMatrixNumpy(CalcMatrix):
    def __init__(self, mat1, mat2):
        self.add = mat1 + mat2              # 加算
        self.sub = mat1 - mat2              # 減算
        self.mul = mat1 * mat2              # 積(アダマール積)
        self.transpose = mat2.transpose(0, 2, 1)        # 転置
        self.dot = np.dot(mat1, self.transpose)         # 内積1
        self.matmul = np.matmul(mat1, self.transpose)   # 内積2
        self.det = np.linalg.det(self.matmul)   # 行列式
        self.inv = np.linalg.inv(self.matmul)   # 逆行列
        x = np.radians(mat1 * 360)
        self.sin = np.sin(x)
        self.cos = np.cos(x)
        self.tan = np.tan(x)
        return

class CalcMatrixTf(CalcMatrix):
    def __init__(self, mat1, mat2):
        tf_mat1 = tf.compat.v1.placeholder(tf.float32, shape=mat1.shape)
        tf_mat2 = tf.compat.v1.placeholder(tf.float32, shape=mat2.shape)

        tf_add = tf.add(tf_mat1, tf_mat2)       # 加算
        tf_sub = tf.subtract(tf_mat1, tf_mat2)  # 減算
        tf_mul = tf.multiply(tf_mat1, tf_mat2)  # 積(アダマール積)
        tf_transpose = tf.compat.v1.transpose(tf_mat2, perm=[0, 2, 1])  # 転置
        tf_dot = tf.tensordot(tf_mat1, tf_transpose, [[2], [1]])    # 内積1
        tf_matmul = tf.matmul(tf_mat1, tf_transpose)    # 内積2
        tf_det = tf.linalg.det(tf_matmul)       # 行列式
        tf_inv = tf.linalg.inv(tf_matmul)       # 逆行列
#        x = tf.constant([30. * 0.017453292519943295, 45. * 0.017453292519943295, 60. * 0.017453292519943295, 90. * 0.017453292519943295])
        x = self.tf_radians(mat1 * 360)
        tf_sin = tf.compat.v1.math.sin(x)
        tf_cos = tf.compat.v1.math.cos(x)
        tf_tan = tf.compat.v1.math.tan(x)

        sess = tf.compat.v1.Session()
        self.add, self.sub, self.mul, self.transpose, self.dot, self.matmul, self.det, self.inv, \
        self.sin, self.cos, self.tan = \
                sess.run([tf_add, tf_sub, tf_mul, \
                          tf_transpose, \
                          tf_dot, tf_matmul, \
                          tf_det, tf_inv, \
                          tf_sin, tf_cos, tf_tan], feed_dict={tf_mat1:mat1, tf_mat2:mat2})
        sess.close()

        return

    def tf_radians(self, deg):
        return tf.convert_to_tensor(deg * 0.017453292519943295) # 2pi/360

def main():
    # --- 引数処理 ---
    args = ArgParser()

    # --- 行列計算用の数値を生成 ---
    mat1 = np.random.rand(3, 5, 7).astype(np.float32)
    mat2 = np.random.rand(3, 5, 7).astype(np.float32)
    print('<< Input Matrix >>')
    print('mat1 = {}'.format(mat1))
    print('mat2 = {}'.format(mat2))

    # --- Numpyで計算 ---
    calc_mat_np = CalcMatrixNumpy(mat1, mat2)
    calc_mat_np.show()

    # --- TensorFlowで計算 ---
    calc_mat_tf = CalcMatrixTf(mat1, mat2)
    calc_mat_tf.show()

    # --- それぞれの算出結果を比較 ---
    print('<< Check Error >>')
    print('add : {}'.format(np.max(np.abs(calc_mat_np.add-calc_mat_tf.add))))
    print('sub : {}'.format(np.max(np.abs(calc_mat_np.sub-calc_mat_tf.sub))))
    print('mul : {}'.format(np.max(np.abs(calc_mat_np.mul-calc_mat_tf.mul))))
    print('transpose : {}'.format(np.max(np.abs(calc_mat_np.transpose-calc_mat_tf.transpose))))
    print('dot : {}'.format(np.max(np.abs(calc_mat_np.dot-calc_mat_tf.dot))))
    print('matmul : {}'.format(np.max(np.abs(calc_mat_np.matmul-calc_mat_tf.matmul))))
    print('det : {}'.format(np.max(np.abs(calc_mat_np.dot-calc_mat_tf.dot))))
    print('inv : {}'.format(np.max(np.abs(calc_mat_np.inv-calc_mat_tf.inv))))
    print('sin : {}'.format(np.max(np.abs(calc_mat_np.sin-calc_mat_tf.sin))))
    print('cos : {}'.format(np.max(np.abs(calc_mat_np.cos-calc_mat_tf.cos))))
    print('tan : {}'.format(np.max(np.abs(calc_mat_np.tan-calc_mat_tf.tan))))

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


