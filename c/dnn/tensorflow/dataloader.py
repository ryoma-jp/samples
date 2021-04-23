# -*- coding: utf-8 -*-

import os
import random
import cv2
import numpy as np

class DataLoader():
	# --- constant ---
	TYPE_CIFAR10 = 'cifar10'
	
	def __init__(self, data_type=TYPE_CIFAR10, data_dir=None, validation_ratio=0.1):
		'''
			type: data type('cifar10', ...(T.B.D))
			dir: dataset directory
			validation_ratio: validation data ratio against training data
		'''
		
		def __set_data(train_data=None, train_label=None, test_data=None, test_label=None, validation_ratio=0.1):
			self.train_data = train_data
			self.train_label = train_label
			self.test_data = test_data
			self.test_label = test_label
			
			if (self.train_data is not None):
				self.n_train_data = len(self.train_data)
				self.idx_train_data = list(range(self.n_train_data))
			else:
				self.n_train_data = 0
				self.idx_train_data = []
			
			if (self.test_data is not None):
				self.n_test_data = len(self.test_data)
				self.idx_test_data = list(range(self.n_test_data))
			else:
				self.n_test_data = 0
				self.idx_test_data = []
			
			return
		
		self.data_type = data_type
		if (data_type == self.TYPE_CIFAR10):
			def unpickle(file):
				import pickle
				with open(file, 'rb') as f:
					dict = pickle.load(f, encoding='bytes')
				return dict
			
			identity = np.eye(10, dtype=np.int)
			
			# --- load train data ---
			train_files = ['data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4', 'data_batch_5']
			dataset = unpickle(os.path.join(data_dir, train_files[0]))
			train_images = dataset[b'data']
			train_labels = [identity[i] for i in dataset[b'labels']]
			for train_file in train_files[1:]:
				dataset = unpickle(os.path.join(data_dir, train_file))
				train_images = np.vstack((train_images, dataset[b'data']))
				train_labels = np.vstack((train_labels, [identity[i] for i in dataset[b'labels']]))
			
			# --- load test data ---
			dataset = unpickle(os.path.join(data_dir, 'test_batch'))
			test_images = dataset[b'data']
			test_labels = np.array([identity[i] for i in dataset[b'labels']])
			
			# --- transpose: [N, C, H, W] -> [N, H, W, C] ---
			train_images = train_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
			test_images = test_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
			
			# --- normalization ---
#			train_images = train_images / 255
#			test_images = test_images / 255
#			train_mean = np.mean(train_images, axis=(0, 1, 2))
#			train_std = np.std(train_images, axis=(0, 1, 2))
#			
#			test_mean = np.mean(test_images, axis=(0, 1, 2))
#			test_std = np.std(test_images, axis=(0, 1, 2))
#			
#			for i in range(3):
#				train_images[:, :, :, i] = (train_images[:, :, :, i] - train_mean[i]) / train_std[i]
#				test_images[:, :, :, i] = (test_images[:, :, :, i] - train_mean[i]) / train_std[i]
			
			__set_data(train_images, train_labels, test_images, test_labels, validation_ratio)
		else:
			print('[ERROR] unknown type: {}'.format(type))
			__set_data()
		
		return

	def get_normalized_data(self, data_type):
		"""
			data_type: type of data('train', 'validation', 'test')
		"""
		if (data_type == 'train'):
			return self.train_data / 255
		elif (data_type == 'validation'):
			# T.B.D
			pass
		else:
			return self.test_data / 255
	
	def next_batch(self, n_minibatch):
		def random_erasing(img):
			size = [random.randint(3, 10) for _i in range(2)]
			pos = [np.clip(random.randint(0, img.shape[i]), 0, img.shape[i]-size[i]) for i in range(2)]
			color = random.randint(0, 255)
			img_erased = img
			if (random.randint(0, 1) == 0):
				img_erased[pos[0]:pos[0]+size[0], pos[1]:pos[1]+size[1], :] = color

			return img_erased

		def img_scaling(img, rate):
			"""
				img: image
				rate: rate
			"""
			h, w = img.shape[:2]
			src = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0]], np.float32)
			dest = src * rate
			affine = cv2.getAffineTransform(src, dest)
			affine[:2, 2] += (np.array([w, h], dtype=np.float32)*(1-rate))/2.0
			return cv2.warpAffine(img, affine, (w, h), cv2.INTER_LANCZOS4)
		
		def img_rotate(img, angle):
			"""
				img: image
				angle: angle [deg]
			"""
			h, w = img.shape[:2]
			affine = cv2.getRotationMatrix2D((w/2.0, h/2.0), angle, 1.0)
			return cv2.warpAffine(img, affine, (w, h))
		
		def img_shift(img, shifts):
			"""
				img: image
				shifts: shift [pixel]
			"""
			h, w = img.shape[:2]
			src = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0]], np.float32)
			dest = src + shifts.reshape(1, -1).astype(np.float32)
			affine = cv2.getAffineTransform(src, dest)
			return cv2.warpAffine(img, affine, (w, h))

		index = random.sample(self.idx_train_data, n_minibatch)
		train_data = self.train_data[index]
		train_label = self.train_label[index]
		
		if (self.data_type == self.TYPE_CIFAR10):
			# --- random flip ---
			#   0: none
			#   1: up down
			#   2: left right
			#   3: up down and left right
#			flip_idx = [0, 1, 2, 3]
			flip_idx = [0, 2]
			
			# --- brightness ---
			#   x0.8 to x1.2
			brightness_coef = 0.2
			
			# --- scaling ---
			#   x0.8 to x1.2
			scaling_coef = 0.2
			
			# --- rotation ---
			#   -15deg to +15deg
			rotation_coef = 15
			
			# --- shift ---
			#   -2pix to +2pix
			shift_coef = 2
			
			for i in range(n_minibatch):
				np.random.shuffle(flip_idx)
				brightness = random.randint(-(brightness_coef * 255), brightness_coef * 255)  # ((random.random()-0.5) * brightness_coef) * 255
				angle = random.randint(-rotation_coef, rotation_coef)  # (random.random()-0.5) * rotation_coef
				shifts = np.array([random.randint(-shift_coef, shift_coef) for i in range(2)])  # np.array([(random.random()-0.5)*shift_coef, (random.random()-0.5)*shift_coef], dtype=np.int)
				scale_rate = ((random.random()-0.5) * 2.0 * scaling_coef) + 1.0
				train_data[i] = random_erasing(train_data[i].copy())
				train_data[i] = img_scaling(train_data[i], scale_rate)
#				train_data[i] = img_rotate(train_data[i], angle)
				train_data[i] = img_shift(train_data[i], shifts)

				if (flip_idx[0] == 0):
					train_data[i] = np.clip(train_data[i] + brightness, 0, 255)
				elif (flip_idx[0] == 1):
					train_data[i] = np.clip(np.flipud(train_data[i]) + brightness, 0, 255)
				elif (flip_idx[0] == 2):
					train_data[i] = np.clip(np.fliplr(train_data[i]) + brightness, 0, 255)
				else:
					train_data[i] = np.clip(np.flipud(np.fliplr(train_data[i])) + brightness, 0, 255)
		
		return train_data / 255, train_label

