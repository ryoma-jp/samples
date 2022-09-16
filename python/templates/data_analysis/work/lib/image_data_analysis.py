"""Image Data Analysis

画像データ分析用モジュール
"""

import numpy as np

def get_mean_images(x, y, label_names):
    """get_mean_images

    平均画像を取得する
    
    Args:
        x (numpy.ndarray): 入力画像群 [NHWC], C=RGB
        y (numpy.ndarray): 正解ラベル
        label_names: ラベル名

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
    