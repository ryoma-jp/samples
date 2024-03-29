""" 位置エンコーディング
"""

import numpy as np
import tensorflow as tf

def get_angles(pos, i, d_model):
	angle_rates = 1 / np.power(10000, (2 * (i//2)) / np.float32(d_model))
	return pos * angle_rates

def positional_encoding(position, d_model):
	angle_rads = get_angles(np.arange(position)[:, np.newaxis],
		np.arange(d_model)[np.newaxis, :],
		d_model)

	# 配列中の偶数インデックスにはsinを適用; 2i
	angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])

	# 配列中の奇数インデックスにはcosを適用; 2i+1
	angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])

	pos_encoding = angle_rads[np.newaxis, ...]

	return tf.cast(pos_encoding, dtype=tf.float32)


