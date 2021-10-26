#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import numpy as np

#---------------------------------
# 関数: create_signal
#   フィルタ動作確認用波形生成
# 引数説明：
#   fs: サンプリング周波数
#   duration: 時間長[sec]
#---------------------------------
def create_signal(fs=100000, duration=1):
    n_samples = fs * duration

    t = np.arange(n_samples) / fs
    y = np.random.normal(loc=0, scale=1, size=n_samples)
    y = y / max(np.abs(y))
#    y = np.random.rand(n_samples)

#    print(min(y), max(y))

    return t, y
