""" Trainer
"""

import time
import tensorflow as tf
from .masking import create_masks
from .model import Transformer

class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):
	def __init__(self, d_model, warmup_steps=4000):
		super(CustomSchedule, self).__init__()

		self.d_model = d_model
		self.d_model = tf.cast(self.d_model, tf.float32)

		self.warmup_steps = warmup_steps

	def __call__(self, step):
		arg1 = tf.math.rsqrt(step)
		arg2 = step * (self.warmup_steps ** -1.5)

		return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)

class Trainer():
	def __init__(self, input_vocab_size, target_vocab_size,
					num_layers=4,
					d_model=128,
					dff=512,
					num_heads=8,
					dropout_rate=0.1):
		
		# --- モデル ---
		self.model = Transformer(num_layers, d_model, num_heads, dff,
								input_vocab_size, target_vocab_size, 
								pe_input=input_vocab_size, 
								pe_target=target_vocab_size,
								rate=dropout_rate)
		
		# --- オプティマイザ ---
		learning_rate = CustomSchedule(d_model)
		self.optimizer = tf.keras.optimizers.Adam(learning_rate, beta_1=0.9, beta_2=0.98, epsilon=1e-9)
		
		# --- 損失関数 ---
		self.loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')
		
		# --- 学習メトリクス ---
		self.train_loss = tf.keras.metrics.Mean(name='train_loss')
		self.train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

	def loss_function(self, real, pred):
		mask = tf.math.logical_not(tf.math.equal(real, 0))
		loss_ = self.loss_object(real, pred)

		mask = tf.cast(mask, dtype=loss_.dtype)
		loss_ *= mask

		return tf.reduce_mean(loss_)


	train_step_signature = [
		tf.TensorSpec(shape=(None, None), dtype=tf.int64),
		tf.TensorSpec(shape=(None, None), dtype=tf.int64),
	]
	@tf.function(input_signature=train_step_signature)
	def train_step(self, inp, tar):
		tar_inp = tar[:, :-1]
		tar_real = tar[:, 1:]

		enc_padding_mask, combined_mask, dec_padding_mask = create_masks(inp, tar_inp)

		with tf.GradientTape() as tape:
			predictions, _ = self.model(inp, tar_inp, 
										True, 
										enc_padding_mask, 
										combined_mask, 
										dec_padding_mask)
			loss = self.loss_function(tar_real, predictions)

		gradients = tape.gradient(loss, self.model.trainable_variables)    
		self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))

		self.train_loss(loss)
		self.train_accuracy(tar_real, predictions)



	def training(self, train_dataset, epochs=20):
		checkpoint_path = "./checkpoints/train"
		ckpt = tf.train.Checkpoint(transformer=self.model, optimizer=self.optimizer)
		ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)

		# チェックポイントが存在したなら、最後のチェックポイントを復元
		if ckpt_manager.latest_checkpoint:
			ckpt.restore(ckpt_manager.latest_checkpoint)
			print ('Latest checkpoint restored!!')

		for epoch in range(epochs):
			start = time.time()

			self.train_loss.reset_states()
			self.train_accuracy.reset_states()

			# inp -> portuguese, tar -> english
			for (batch, (inp, tar)) in enumerate(train_dataset):
				self.train_step(inp, tar)

				if batch % 50 == 0:
					print ('Epoch {} Batch {} Loss {:.4f} Accuracy {:.4f}'.format(
						epoch + 1, batch, self.train_loss.result(), self.train_accuracy.result()))

			if (epoch + 1) % 5 == 0:
				ckpt_save_path = ckpt_manager.save()
				print ('Saving checkpoint for epoch {} at {}'.format(epoch+1, ckpt_save_path))

			print ('Epoch {} Loss {:.4f} Accuracy {:.4f}'.format(epoch + 1, 
						self.train_loss.result(), 
						self.train_accuracy.result()))

			print ('Time taken for 1 epoch: {} secs\n'.format(time.time() - start))


