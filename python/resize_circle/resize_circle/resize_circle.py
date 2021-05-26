#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np
import cv2
from PIL import Image

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


