""" Attention
"""

import tensorflow as tf

def scaled_dot_product_attention(q, k, v, mask):
	""" アテンションの重みの計算
		q, k, vは最初の次元が一致していること
		k, vは最後から2番めの次元が一致していること
		マスクは型（パディングかルックアヘッドか）によって異なるshapeを持つが、
		加算の際にブロードキャスト可能であること
		引数：
			q: query shape == (..., seq_len_q, depth)
			k: key shape == (..., seq_len_k, depth)
			v: value shape == (..., seq_len_v, depth_v)
			mask: (..., seq_len_q, seq_len_k) にブロードキャスト可能な
				shapeを持つ浮動小数点テンソル。既定値はNone

		戻り値：
			出力、アテンションの重み
	"""

	matmul_qk = tf.matmul(q, k, transpose_b=True)  # (..., seq_len_q, seq_len_k)

	# matmul_qkをスケール
	dk = tf.cast(tf.shape(k)[-1], tf.float32)
	scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)

	# マスクをスケール済みテンソルに加算
	if mask is not None:
		scaled_attention_logits += (mask * -1e9)  

	# softmax は最後の軸(seq_len_k)について
	# 合計が1となるように正規化
	attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)  # (..., seq_len_q, seq_len_k)

	output = tf.matmul(attention_weights, v)  # (..., seq_len_q, depth_v)

	return output, attention_weights

class MultiHeadAttention(tf.keras.layers.Layer):
	def __init__(self, d_model, num_heads):
		super(MultiHeadAttention, self).__init__()
		self.num_heads = num_heads
		self.d_model = d_model

		assert d_model % self.num_heads == 0

		self.depth = d_model // self.num_heads

		self.wq = tf.keras.layers.Dense(d_model)
		self.wk = tf.keras.layers.Dense(d_model)
		self.wv = tf.keras.layers.Dense(d_model)

		self.dense = tf.keras.layers.Dense(d_model)

	def split_heads(self, x, batch_size):
		""" 最後の次元を(num_heads, depth)に分割。
			結果をshapeが(batch_size, num_heads, seq_len, depth)となるようにリシェイプする。
		"""
		x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
		return tf.transpose(x, perm=[0, 2, 1, 3])

	def call(self, v, k, q, mask):
		batch_size = tf.shape(q)[0]

		q = self.wq(q)  # (batch_size, seq_len, d_model)
		k = self.wk(k)  # (batch_size, seq_len, d_model)
		v = self.wv(v)  # (batch_size, seq_len, d_model)

		q = self.split_heads(q, batch_size)  # (batch_size, num_heads, seq_len_q, depth)
		k = self.split_heads(k, batch_size)  # (batch_size, num_heads, seq_len_k, depth)
		v = self.split_heads(v, batch_size)  # (batch_size, num_heads, seq_len_v, depth)

		# scaled_attention.shape == (batch_size, num_heads, seq_len_q, depth)
		# attention_weights.shape == (batch_size, num_heads, seq_len_q, seq_len_k)
		scaled_attention, attention_weights = scaled_dot_product_attention(q, k, v, mask)

		scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])  # (batch_size, seq_len_q, num_heads, depth)

		concat_attention = tf.reshape(scaled_attention, 
			(batch_size, -1, self.d_model))  # (batch_size, seq_len_q, d_model)

		output = self.dense(concat_attention)  # (batch_size, seq_len_q, d_model)

		return output, attention_weights
