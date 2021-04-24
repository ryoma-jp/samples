# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import yaml

class TF_Model():
	def __init__(self):
		tf.compat.v1.disable_eager_execution()
		
		return
	
	def conv_net(self, input_dims, conv_channels, conv_kernel_size, pool_size, fc_channels, output_dims, dropout_rate, is_train):
		"""
			input_dims: input dims [N, H, W, C]
			conv_channels: convolution filter channels [<layer1 channel>, <layer2 channel>, ...]
			conv_kernel_size: convolution filter size [<layer1 kernel size>, <layer2 kernel size>, ...]
			pool_size: pooling size [<layer1 pool size>, <layer2 kernel size>, ...]
			fc_channels: fully connected channels [<layer1 channel>, <layer2 channel>, ...]
			output_dims: output dims
		"""

		def weight_variable(shape, scope, id=0):
			init = tf.compat.v1.truncated_normal_initializer(mean=0.0, stddev=0.01)
			with tf.compat.v1.variable_scope(scope, reuse=tf.compat.v1.AUTO_REUSE):
				var = tf.compat.v1.get_variable('Weight{}'.format(id), shape=shape, initializer=init)

		def bias_variable(shape, scope, id=0):
			init = tf.constant_initializer([0])
			with tf.compat.v1.variable_scope(scope, reuse=tf.compat.v1.AUTO_REUSE):
				var = tf.compat.v1.get_variable('Bias{}'.format(id), shape=shape, initializer=init)

		def bn_variables(shape, scope):
			with tf.compat.v1.variable_scope(scope, reuse=tf.compat.v1.AUTO_REUSE):
				gamma = tf.compat.v1.get_variable('gamma', shape[-1], initializer=tf.constant_initializer(1.0))
				beta = tf.compat.v1.get_variable('beta', shape[-1], initializer=tf.constant_initializer(0.0))
				moving_avg = tf.compat.v1.get_variable('moving_avg', shape[-1], initializer=tf.constant_initializer(0.0), trainable=False)
				moving_var = tf.compat.v1.get_variable('moving_var', shape[-1], initializer=tf.constant_initializer(1.0), trainable=False)

		def batch_norm(x, scope, train, epsilon=0.001, decay=0.99):
			if train:
				with tf.compat.v1.variable_scope(scope, reuse=tf.compat.v1.AUTO_REUSE):
					shape = x.get_shape().as_list()
					ema = tf.compat.v1.train.ExponentialMovingAverage(decay=decay)
					batch_avg, batch_var = tf.compat.v1.nn.moments(x, list(range(len(shape)-1)))

					print(batch_avg.name)
					print(batch_var.name)
					print(ema.name)
					print(x.name)

					ema_apply_op = ema.apply([batch_avg, batch_var])

			with tf.compat.v1.variable_scope(scope, reuse=True):
				gamma, beta = tf.compat.v1.get_variable('gamma'), tf.compat.v1.get_variable('beta')
				moving_avg, moving_var = tf.compat.v1.get_variable('moving_avg'), tf.compat.v1.get_variable('moving_var')
				control_inputs = []
				if train:
					with tf.control_dependencies([ema_apply_op]):
						avg = moving_avg.assign(ema.average(batch_avg))
						var = moving_var.assign(ema.average(batch_var))

						with tf.control_dependencies([avg, var]):
							control_inputs = [moving_avg, moving_var]
				else:
					avg = moving_avg
					var = moving_var
				with tf.control_dependencies(control_inputs):
					output = tf.compat.v1.nn.batch_normalization(x, avg, var, offset=beta, scale=gamma, variance_epsilon=epsilon)

			return output

		def conv2d(x, scope, id):
			with tf.compat.v1.variable_scope(scope, reuse=True):
				W = tf.compat.v1.get_variable('Weight{}'.format(id))
				b = tf.compat.v1.get_variable('Bias{}'.format(id))
				return tf.compat.v1.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME') + b

		def affine(x, scope, id=0):
			with tf.compat.v1.variable_scope(scope, reuse=True):
				W = tf.compat.v1.get_variable('Weight{}'.format(id))
				b = tf.compat.v1.get_variable('Bias{}'.format(id))
				return tf.matmul(x, W) + b

		def max_pool(x, size):
			return tf.compat.v1.nn.max_pool(x, ksize=[1, size, size, 1], strides=[1, size, size, 1], padding='SAME')

		x = tf.compat.v1.placeholder(tf.float32, shape=input_dims)
		y_ = tf.compat.v1.placeholder(tf.float32, shape=output_dims)

		# convolution layer
		h_out = x
		h_out_shape = input_dims[1:]
		prev_channel = input_dims[-1]
		for i, (_conv_channel, _conv_kernel_size, _pool_size) in enumerate(zip(conv_channels, conv_kernel_size, pool_size)):
#			print(_conv_channel, _conv_kernel_size, _pool_size, prev_channel)

			for ii in range(2):
				weight_variable([_conv_kernel_size, _conv_kernel_size, prev_channel, _conv_channel], 'ConvLayer{}'.format(i), ii)
				bias_variable([_conv_channel], 'ConvLayer{}'.format(i), ii)
				h_out = conv2d(h_out, 'ConvLayer{}'.format(i), ii)

				prev_channel = _conv_channel

			h_conv = tf.compat.v1.nn.relu(h_out)
			if (is_train):
				h_conv = tf.compat.v1.layers.dropout(h_conv, dropout_rate)

			#h_out_shape = np.array([h_out_shape[0] / _pool_size, h_out_shape[1] / _pool_size, _conv_channel], dtype=np.int)
			h_conv_shape = h_conv.get_shape().as_list()[1:]
			
			enable_bn = True
			if (enable_bn):
				bn_variables(h_conv_shape, 'ConvLayer{}'.format(i))
				h_bn = batch_norm(h_conv, 'ConvLayer{}'.format(i), is_train, epsilon=1e-5, decay=0.9)

				h_out = max_pool(h_bn, _pool_size)
			else:
				h_out = max_pool(h_conv, _pool_size)
			h_out_shape = h_out.get_shape().as_list()[1:]

			prev_channel = _conv_channel

		# fully connected layer
		h_out = tf.reshape(h_out, [tf.shape(x)[0], -1])
		prev_channel = np.prod(h_out_shape)
		i = 0
		if (fc_channels is not None):
			for i, _fc_channel in enumerate(fc_channels):
				weight_variable([prev_channel, _fc_channel], 'FCLayer{}'.format(i))
				bias_variable([_fc_channel], 'FCLayer{}'.format(i))
				h_out = tf.compat.v1.nn.relu(affine(h_out, 'FCLayer{}'.format(i)))
				if (is_train):
					h_out = tf.compat.v1.layers.dropout(h_out, dropout_rate)
				prev_channel = _fc_channel
			i = i + 1

		weight_variable([prev_channel, output_dims[-1]], 'FCLayer{}'.format(i))
		bias_variable([output_dims[-1]], 'FCLayer{}'.format(i))
		y = affine(h_out, 'FCLayer{}'.format(i))

		if (is_train):
			tf.compat.v1.add_to_collection('train_input', x)
			tf.compat.v1.add_to_collection('train_output', y)
		else:
			# --- standard name is set from the prediction model ---
			tf.compat.v1.add_to_collection('input', x)
			tf.compat.v1.add_to_collection('output', y)

		return x, y, y_

	def get_ops(self, outfile, inference_ops=None):
		"""
			outfile: オペレーション出力先
			inference_ops: 推論グラフのオペレーション
							[0]: input, [1]: output
		"""
		graph = tf.compat.v1.get_default_graph()
		all_ops = graph.get_operations()
		flg_inference_ops = False
		
		with open(outfile, 'w') as f:
			ret_ops = []
			for _op in all_ops:
#				f.write('{}'.format(_op.op_def))
#				if ((_op.op_def.name == 'MatMul') or (_op.op_def.name == 'Add')):
#					f.write('<< {} >>\n'.format(_op.op_def.name))
#					for _input in _op.inputs:
#						f.write(' * {}\n'.format(_input))
				if (flg_inference_ops):
					if ((_op.op_def.name == 'Conv2D') or (_op.op_def.name == 'AddV2')):
						ret_ops.append(_op)
					if (inference_ops[1] in _op.name):
						flg_inference_ops = False
				else:
					if (inference_ops[0] in _op.name):
						flg_inference_ops = True
						if ((_op.op_def.name == 'Conv2D') or (_op.op_def.name == 'AddV2')):
							ret_ops.append(_op)
				f.write('{}\n'.format(_op))
		
		return ret_ops

	def fit(self, dataset,
				train_x, train_y, train_y_, 
				test_x, test_y, test_y_, 
				n_epoch=32, n_minibatch=32,
				optimizer='SGD', learning_rate=0.001,
				weight_decay=0.001,
				model_dir='model'):

		weights = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.TRAINABLE_VARIABLES)
		loss = tf.compat.v1.nn.softmax_cross_entropy_with_logits_v2(labels=train_y_, logits=train_y)
		for weight in weights:
			if ('W_' in weight.name):
				print(weight.name)
				loss = loss + weight_decay * tf.nn.l2_loss(weight)

		if (optimizer == 'SGD'):
			train_step = tf.compat.v1.train.GradientDescentOptimizer(learning_rate).minimize(loss)
		elif (optimizer == 'Adam'):
			train_step = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(loss)
		else:
			print('[ERROR] unknown optimizer: {}'.format(optimizer))
			quit()

		correct_prediction = tf.equal(tf.argmax(train_y, 1), tf.argmax(train_y_, 1))
		train_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		correct_prediction = tf.equal(tf.argmax(test_y, 1), tf.argmax(test_y_, 1))
		test_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		init = tf.compat.v1.initialize_all_variables()
		config = tf.compat.v1.ConfigProto(
			gpu_options=tf.compat.v1.GPUOptions(
				allow_growth = True
			)
		)
		sess = tf.compat.v1.Session(config=config)
		sess.run(init)
		saver = tf.compat.v1.train.Saver()
		
		inference_ops = self.get_ops(os.path.join(model_dir, 'ops.txt'), 
						inference_ops=[test_x.name[:test_x.name.find(':')], test_y.name[:test_y.name.find(':')]])
		print(inference_ops)
		with open(os.path.join(model_dir, 'node_name.yaml'), 'w') as f:
			f.write('input_node_name: \'{}\'\n'.format(test_x.name[:test_x.name.find(':')]))
			f.write('output_node_name: \'{}\'\n'.format(test_y.name[:test_y.name.find(':')]))
			for i, _inference_ops in enumerate(inference_ops):
				f.write('hidden_{}: \'{}\'\n'.format(i+1, _inference_ops.name))

		log_label = ['epoch', 'train_loss', 'test_loss', 'train_acc', 'test_acc']
		log = []
		print(log_label)
		train_data_norm = dataset.get_normalized_data('train')
		test_data_norm = dataset.get_normalized_data('test')
		iter_minibatch = len(train_data_norm) // n_minibatch
		for epoch in range(n_epoch):
			for _iter in range(iter_minibatch):
				batch_x, batch_y = dataset.next_batch(n_minibatch)
				sess.run(train_step, feed_dict={train_x: batch_x, train_y_: batch_y})

			tmp_train_loss, tmp_train_acc = [], []
			sep_len = 10000
			pos = 0
			while (pos+sep_len < len(train_data_norm)):
				_loss = sess.run(loss, feed_dict={train_x: train_data_norm[pos:pos+sep_len], train_y_: dataset.train_label[pos:pos+sep_len]})
				_acc = sess.run(test_accuracy, feed_dict={test_x: train_data_norm[pos:pos+sep_len], test_y_: dataset.train_label[pos:pos+sep_len]})
				tmp_train_loss.append(np.mean(_loss))
				tmp_train_acc.append(_acc)
				pos = pos+sep_len
			_loss = sess.run(loss, feed_dict={train_x: train_data_norm[pos:], train_y_: dataset.train_label[pos:]})
			_acc = sess.run(test_accuracy, feed_dict={test_x: train_data_norm[pos:], test_y_: dataset.train_label[pos:]})
			tmp_train_loss.append(np.mean(_loss))
			tmp_train_acc.append(_acc)
			
			tmp_test_loss = sess.run(loss, feed_dict={train_x: test_data_norm, train_y_: dataset.test_label})
			tmp_test_acc = sess.run(test_accuracy, feed_dict={test_x: test_data_norm, test_y_: dataset.test_label})
			log.append([epoch, np.mean(tmp_train_loss), np.mean(tmp_test_loss), np.mean(tmp_train_acc), tmp_test_acc])
			print(log[-1])

		tmp_train_acc = []
		sep_len = 10000
		pos = 0
		while (pos+sep_len < len(train_data_norm)):
			_acc = sess.run(test_accuracy, feed_dict={test_x: train_data_norm[pos:pos+sep_len], test_y_: dataset.train_label[pos:pos+sep_len]})
			tmp_train_acc.append(_acc)
			pos = pos+sep_len
		_acc = sess.run(test_accuracy, feed_dict={test_x: train_data_norm[pos:], test_y_: dataset.train_label[pos:]})
		tmp_train_acc.append(_acc)
		
		train_acc = np.mean(tmp_train_acc)
		test_acc = sess.run(test_accuracy, feed_dict={test_x: test_data_norm, test_y_: dataset.test_label})

		saver.save(sess, os.path.join(model_dir, 'model.ckpt'))
		pd.DataFrame(log).to_csv(os.path.join(model_dir, 'log.csv'), header=log_label)

		# --- save weights ---
		for weight in weights:
			weight_dir = os.path.join(model_dir, 'weights')
			os.makedirs(weight_dir, exist_ok=True)

			weight_val = sess.run(weight)
			weight_name = weight.name.translate(str.maketrans({'/': '-', ':': '-'}))
			pd.DataFrame(weight_val.reshape(len(weight_val), -1)).to_csv(os.path.join(weight_dir, '{}.csv'.format(weight_name)), header=None, index=None)

			plt.hist(weight_val.reshape(-1), bins=32)
			plt.tight_layout()
			plt.savefig(os.path.join(weight_dir, '{}.png'.format(weight_name)))
			plt.close()

		sess.close()
		tf.compat.v1.reset_default_graph()

		return train_acc, test_acc

	def predict(self, dataset, model):
		config = tf.compat.v1.ConfigProto(
			gpu_options=tf.compat.v1.GPUOptions(
				allow_growth = True
			)
		)
		sess = tf.compat.v1.Session(config=config)

		saver = tf.compat.v1.train.import_meta_graph(model + '.meta', clear_devices=True)
		saver.restore(sess, model)

		x = tf.compat.v1.get_collection('input')[0]
		y = tf.compat.v1.get_collection('output')[0]
		prediction = sess.run(y, feed_dict={x: dataset.get_normalized_data('test')})

		sess.close()
		tf.compat.v1.reset_default_graph()

		return prediction

	def test(self, dataset, model):
		prediction = predict(dataset, model)

		model_dir = str(pathlib.Path(model).resolve().parent)
		compare = np.argmax(prediction, axis=1) == np.argmax(dataset.test_label, axis=1)
		accuracy = len(compare[compare==True]) / len(compare)
		result_csv = np.vstack((np.argmax(prediction, axis=1), np.argmax(dataset.test_label, axis=1))).T
		pd.DataFrame(result_csv).to_csv(os.path.join(model_dir, 'result.csv'), header=['prediction', 'labels'])

		return accuracy

	def tflite_convert(self, saved_model_dir, node_names, output_dir):
		def saved_model_to_frozen_graph(saved_model_dir, saved_model_prefix, output_node_names, output_dir):
			input_meta_graph = os.path.join(saved_model_dir, saved_model_prefix+'.meta')
			checkpoint = os.path.join(saved_model_dir, saved_model_prefix)
			output_graph_filename = os.path.join(output_dir, 'output_graph.pb')

			input_graph = ''
			input_saver_def_path = ''
			input_binary = True
			restore_op_name = ''
			filename_tensor_name = ''
			clear_devices = False

			os.makedirs(output_dir, exist_ok=True)

			'''
				check ops name
			'''
#			config = tf.compat.v1.ConfigProto(
#				gpu_options=tf.compat.v1.GPUOptions(
#					allow_growth = True
#				)
#			)
#			sess = tf.compat.v1.Session(config=config)
#			
#			saver = tf.compat.v1.train.import_meta_graph(input_meta_graph, clear_devices=True)
#			saver.restore(sess, checkpoint)
#		
#			graph = tf.get_default_graph()
#			all_ops = graph.get_operations()
#			
#			outfile = 'ops.txt'
#			with open(outfile, 'w') as f:
#				for _op in all_ops:
#					f.write('{}\n'.format(_op))

			freeze_graph.freeze_graph(
				input_graph, input_saver_def_path, input_binary, checkpoint,
				output_node_names, restore_op_name, filename_tensor_name,
				output_graph_filename, clear_devices, '', '', '', input_meta_graph)

			return output_graph_filename

		def frozen_graph_to_tflite(pb_file, input_node_name, output_node_name, output_dir):
			input_arrays = [input_node_name]
			output_arrays = [output_node_name]

			converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
					pb_file, input_arrays, output_arrays)
			tflite_model = converter.convert()

			output_tflite_filename = os.path.join(output_dir, 'converted_model.tflite')
			open(output_tflite_filename, 'wb').write(tflite_model)

			return output_tflite_filename

		# --- parameters ---
		saved_model_dir = args.saved_model_dir
		saved_model_prefix = args.saved_model_prefix
		node_name_yaml = os.path.join(saved_model_dir, args.node_name_yaml)
		output_dir = args.output_dir

		try:
			with open(node_name_yaml) as f:
				node_name = yaml.safe_load(f)
		except Exception as e:
			print('[ERROR] Exception occurred: {} load failed'.format(node_name_yaml))
			quit()
		input_node_names = node_name['input_node_name']
		output_node_names = node_name['output_node_name']

		pb_file = saved_model_to_frozen_graph(saved_model_dir, saved_model_prefix, output_node_names, output_dir)
		tflite_file = frozen_graph_to_tflite(pb_file, input_node_names, output_node_names, output_dir)
		
		return

	def inference(self, tflite_file, input_data):
		interpreter = tf.compat.v1.lite.Interpreter(model_path=tflite_file)
		interpreter.allocate_tensors()

		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()

		input_shape = input_details[0]['shape']
		print(input_shape)
		print(input_data.shape)
		print(input_data.dtype)

		output_data = []
		for _i, _input_data in enumerate(input_data):
			if (((_i+1) % 1000) == 0):
				print('{} of {}'.format((_i+1), len(input_data)))
			interpreter.set_tensor(input_details[0]['index'], _input_data.reshape(input_shape))
			interpreter.invoke()
			output_data.append(np.argmax(interpreter.get_tensor(output_details[0]['index'])))

		return np.array(output_data)

