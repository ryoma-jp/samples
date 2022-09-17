"""Image Data Analysis

画像データ分析用モジュール
"""

import cv2
import numpy as np

def get_mean_images(x, y, label_names):
    """get_mean_images

    平均画像を取得する
    
    Args:
        x (numpy.ndarray): 入力画像群 [NHWC], C=RGB
        y (numpy.ndarray): 正解ラベル
        label_names (list): ラベル名

    Returns:
        平均画像

        - img_mean(numpy.ndarray): 平均画像 [NHWC]
        - img_mean_r(numpy.ndarray): R平均画像 [NHWC]
        - img_mean_g(numpy.ndarray): G平均画像 [NHWC]
        - img_mean_b(numpy.ndarray): B平均画像 [NHWC]
    """

    mask_r = [1, 0, 0]
    mask_g = [0, 1, 0]
    mask_b = [0, 0, 1]
    n_classes = len(label_names)
    
    img_mean = []
    img_mean_r = []
    img_mean_g = []
    img_mean_b = []
    for label_id in range(n_classes):
        label_idx = np.arange(len(y))[y==label_id]
        train_images = x[label_idx]

        _img_mean = train_images.mean(axis=0).astype(int)
        img_mean.append(_img_mean)
        img_mean_r.append(_img_mean * mask_r)
        img_mean_g.append(_img_mean * mask_g)
        img_mean_b.append(_img_mean * mask_b)
    
    img_mean = np.array(img_mean)
    img_mean_r = np.array(img_mean_r)
    img_mean_g = np.array(img_mean_g)
    img_mean_b = np.array(img_mean_b)
    
    return img_mean, img_mean_r, img_mean_g, img_mean_b
    
def get_pixel_hist(x, y, label_names, bins):
    """get_pixel_count

    画素値のヒストグラムを取得する
    
    Args:
        x (numpy.ndarray): 入力画像群 [NHWC], C=RGB
        y (numpy.ndarray): 正解ラベル
        label_names (list): ラベル名
        bins (uint8): ヒストグラムのbin数

    Returns:
        クラスごとの画素値のヒストグラムを，RGB，HSV，YUVそれぞれに対する計算結果を返す
        
        ヒストグラムはdict形式で，度数は'frequency'，階数境界は'floor_boundary'である．
        度数はChannelごと・クラスごとに計算し，shapeは[チャネル数(RGB, HSV, or YUV), クラス数, bins]である．

        - pixel_hist_rgb (dict): RGBヒストグラム
        - pixel_hist_hsv (dict): HSVヒストグラム
        - pixel_hist_yuv (dict): YUVヒストグラム
    """
    
    pixel_hist_rgb = None
    pixel_hist_hsv = None
    pixel_hist_yuv = None
    
    n_classes = len(label_names)
    rgb_hist = {'r': [], 'g': [], 'b': []}
    hsv_hist = {'h': [], 's': [], 'v': []}
    yuv_hist = {'y': [], 'u': [], 'v': []}
    for label_id in range(n_classes):
        label_idx = np.arange(len(y))[y==label_id]
        train_images = x[label_idx]
        train_images_hsv = np.array([cv2.cvtColor(img, cv2.COLOR_RGB2HSV) for img in train_images])
        train_images_yuv = np.array([cv2.cvtColor(img, cv2.COLOR_RGB2YUV) for img in train_images])
        
        _r = np.histogram(train_images[:, :, :, 0], bins, range=(0, 255))
        _g = np.histogram(train_images[:, :, :, 1], bins, range=(0, 255))
        _b = np.histogram(train_images[:, :, :, 2], bins, range=(0, 255))
        
        rgb_hist['r'].append(_r[0])
        rgb_hist['g'].append(_g[0])
        rgb_hist['b'].append(_b[0])
        
        _h = np.histogram(train_images_hsv[:, :, :, 0], bins, range=(0, 255))
        _s = np.histogram(train_images_hsv[:, :, :, 1], bins, range=(0, 255))
        _v = np.histogram(train_images_hsv[:, :, :, 2], bins, range=(0, 255))
        
        hsv_hist['h'].append(_h[0])
        hsv_hist['s'].append(_s[0])
        hsv_hist['v'].append(_v[0])
        
        _y = np.histogram(train_images_yuv[:, :, :, 0], bins, range=(0, 255))
        _u = np.histogram(train_images_yuv[:, :, :, 1], bins, range=(0, 255))
        _v = np.histogram(train_images_yuv[:, :, :, 2], bins, range=(0, 255))
        
        yuv_hist['y'].append(_y[0])
        yuv_hist['u'].append(_u[0])
        yuv_hist['v'].append(_v[0])
        
    floor_boundary = [f'{_r[1][i]}-{_r[1][i+1]}' for i in range(bins)]
    
    pixel_hist_rgb = {
        'frequency': np.vstack(([rgb_hist['r']], [rgb_hist['g']], [rgb_hist['b']])),
        'floor_boundary': np.array(floor_boundary)
    }
    
    pixel_hist_hsv = {
        'frequency': np.vstack(([hsv_hist['h']], [hsv_hist['s']], [hsv_hist['v']])),
        'floor_boundary': np.array(floor_boundary)
    }
    
    pixel_hist_yuv = {
        'frequency': np.vstack(([yuv_hist['y']], [yuv_hist['u']], [yuv_hist['v']])),
        'floor_boundary': np.array(floor_boundary)
    }
    
    return pixel_hist_rgb, pixel_hist_hsv, pixel_hist_yuv
