#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from torchvision import transforms

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------

#---------------------------------
# クラス
#---------------------------------
class ResizeCircle():
	def __init__(self, output_dir='./output'):
		# --- 出力ディレクトリ生成 ---
		self.output_dir = output_dir
		os.makedirs(self.output_dir, exist_ok=True)
		
		# --- 円のイメージデータを作成 ---
		img_circle = np.zeros((128, 128, 3), dtype='uint8') + 255
		self.img_circle = cv2.circle(img_circle, (128//2, 128//2), 50, (0, 0, 0), 1)
		cv2.imwrite(os.path.join(self.output_dir, 'base_image.png'), self.img_circle)
		
		# --- リサイズ後のサイズ ---
		self.dsize = [16, 16]
		
		return

	def resize_opencv(self):
		img = cv2.resize(self.img_circle, self.dsize, interpolation=cv2.INTER_NEAREST)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_opencv_nearest.png'), img)
		
		img = cv2.resize(self.img_circle, self.dsize, interpolation=cv2.INTER_LINEAR)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_opencv_linear.png'), img)
		
		img = cv2.resize(self.img_circle, self.dsize, interpolation=cv2.INTER_AREA)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_opencv_area.png'), img)
		
		img = cv2.resize(self.img_circle, self.dsize, interpolation=cv2.INTER_CUBIC)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_opencv_cubic.png'), img)
		
		img = cv2.resize(self.img_circle, self.dsize, interpolation=cv2.INTER_LANCZOS4)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_opencv_lanczos4.png'), img)
		
		return
	
	def resize_pil(self):
		img = self.img_circle.copy()
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img_base = Image.fromarray(img)
		img_base.save(os.path.join(self.output_dir, 'resize_pil_base.png'))
		
		img = img_base.resize(self.dsize, Image.NEAREST)
		img.save(os.path.join(self.output_dir, 'resize_pil_nearest.png'))
		
		img = img_base.resize(self.dsize, Image.BOX)
		img.save(os.path.join(self.output_dir, 'resize_pil_box.png'))
		
		img = img_base.resize(self.dsize, Image.BILINEAR)
		img.save(os.path.join(self.output_dir, 'resize_pil_bilinear.png'))
		
		img = img_base.resize(self.dsize, Image.HAMMING)
		img.save(os.path.join(self.output_dir, 'resize_pil_hamming.png'))
		
		img = img_base.resize(self.dsize, Image.BICUBIC)
		img.save(os.path.join(self.output_dir, 'resize_pil_bicubic.png'))
		
		img = img_base.resize(self.dsize, Image.LANCZOS)
		img.save(os.path.join(self.output_dir, 'resize_pil_lanczos.png'))
		
		return

	def resize_tensorflow(self):
		physical_devices = tf.config.list_physical_devices('GPU')
		if (len(physical_devices) > 0):
			for device in physical_devices:
				tf.config.experimental.set_memory_growth(device, True)
		else:
			print('[ERROR] GPU hardware devices unavailable')
			quit()
		tf_img_base = tf.convert_to_tensor(self.img_circle, tf.uint8)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='area')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_area.png'), img)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='bicubic')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_bicubic.png'), img)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='bilinear')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_bilinear.png'), img)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='gaussian')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_gaussian.png'), img)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='lanczos3')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_lanczos3.png'), img)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='lanczos5')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_lanczos5.png'), img)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='mitchellcubic')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_mitchellcubic.png'), img)
		
		img = tf.image.resize(tf_img_base, self.dsize, method='nearest')
		img = img.numpy().astype(np.uint8)
		cv2.imwrite(os.path.join(self.output_dir, 'resize_tensorflow_nearest.png'), img)
		
		return

	def resize_pytorch(self):
		img_base = self.img_circle.copy()
		img_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2RGB)
		img_base = Image.fromarray(img_base)
		
		transform = transforms.Resize(self.dsize, interpolation=transforms.InterpolationMode.NEAREST)
		img = transform(img_base)
		img.save(os.path.join(self.output_dir, 'resize_pytorch_nearest.png'))
		
		transform = transforms.Resize(self.dsize, interpolation=transforms.InterpolationMode.BILINEAR)
		img = transform(img_base)
		img.save(os.path.join(self.output_dir, 'resize_pytorch_bilinear.png'))
		
		transform = transforms.Resize(self.dsize, interpolation=transforms.InterpolationMode.BICUBIC)
		img = transform(img_base)
		img.save(os.path.join(self.output_dir, 'resize_pytorch_bicubic.png'))
		
		transform = transforms.Resize(self.dsize, interpolation=transforms.InterpolationMode.BOX)
		img = transform(img_base)
		img.save(os.path.join(self.output_dir, 'resize_pytorch_box.png'))
		
		transform = transforms.Resize(self.dsize, interpolation=transforms.InterpolationMode.HAMMING)
		img = transform(img_base)
		img.save(os.path.join(self.output_dir, 'resize_pytorch_hamming.png'))
		
		transform = transforms.Resize(self.dsize, interpolation=transforms.InterpolationMode.LANCZOS)
		img = transform(img_base)
		img.save(os.path.join(self.output_dir, 'resize_pytorch_lanczos.png'))
		
		return
