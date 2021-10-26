#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy import fftpack
from .create_signal import *

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数: signal_filter
#   フィルタ処理
# 引数説明：
#   x: 入力波形
#   fs: サンプリング周波数
#   freq_pass: 通過域周波数[Hz]
#   freq_stop: 阻止域周波数[Hz]
#   gain_pass: 通過域最大損失[Hz]
#   gain_stop: 阻止域最小損失[Hz]
#   btype: フィルタ種別('lowpass', 'highpass', 'bandpass', 'bandstop')
#---------------------------------
def signal_filter(x, fs, freq_pass, freq_stop, gain_pass, gain_stop, btype):
    fn = fs / 2
    freq_pass_norm = freq_pass / fn
    freq_stop_norm = freq_stop / fn

    N, Wn = signal.buttord(freq_pass_norm, freq_stop_norm, gain_pass, gain_stop)
    b, a = signal.butter(N, Wn, btype=btype)

    y = signal.filtfilt(b, a, x)

    return y

#---------------------------------
# 関数: fft
#   FFT
# 引数説明：
#   t: 波形の時刻情報
#   data: 波形データ
#---------------------------------
def signal_fft(t, data):
    duration = (t[1]-t[0]) * len(t)
#    print(duration)
    fs = 1 / (t[1]-t[0])
    freq_list = np.array([_f / len(t) * fs for _f in range(len(t))])

    data_fft = fftpack.fft(data)
#    print(len(data_fft))
#    print(len(freq_list))

#    freq_list2 = fftpack.fftfreq(len(t), d=t[1]-t[0])
#    print(len(freq_list), freq_list[0:len(freq_list)//2])
#    print(len(freq_list2), freq_list2[0:len(freq_list2)//2])

    return freq_list[0:len(t)//2], data_fft[0:len(t)//2]    # 折り返し成分は返さない

#---------------------------------
# 関数: main
#   メイン関数
#---------------------------------
def main():
    def _arg_parser():
        parser = argparse.ArgumentParser(description='信号のLPF，HPFのサンプル\n'
                                                     ' * default: LPF, カットオフ周波数 6kHz, Slope -20dB/decade', 
                    formatter_class=argparse.RawTextHelpFormatter)

        # --- 引数を追加 ---
        parser.add_argument('--filter_type', dest='filter_type', type=str, default='lowpass', required=False, \
                help='フィルタ種別(lowpass, highpass)')
        parser.add_argument('--fs', dest='fs', type=float, default=10000, required=False, \
                help='サンプリングレート[Hz]')
        parser.add_argument('--freq_pass', dest='freq_pass', type=float, default=3000, required=False, \
                help='通過域端周波数[Hz]')
        parser.add_argument('--freq_stop', dest='freq_stop', type=float, default=6000, required=False, \
                help='阻止域端周波数[Hz]')
        parser.add_argument('--gain_pass', dest='gain_pass', type=float, default=3, required=False, \
                help='通過域最大損失[dB]')
        parser.add_argument('--gain_stop', dest='gain_stop', type=float, default=40, required=False, \
                help='阻止域最大損失[dB]')

        args = parser.parse_args()

        return args

    # --- 引数処理 ---
    args = _arg_parser()

    # --- 信号生成 ---
    t, data = create_signal(args.fs, 1)
    freq, data_fft = fft(t, data)
    plt.figure()
    plt.plot(t, data)
    plt.savefig('input.png')
    plt.close()

#    print(data_fft)

    plt.figure()
    plt.plot(freq, data_fft.real)
    plt.savefig('input_fft_real.png')
    plt.close()

    data_fft_amp = np.sqrt(np.power(data_fft.real, 2) + np.power(data_fft.imag, 2))
    plt.figure()
    plt.plot(freq, data_fft_amp)
    plt.savefig('input_fft_amp.png')
    plt.close()

    data_fft_amp_gain = 20 * np.log10(data_fft_amp)
    plt.figure()
    plt.plot(freq, data_fft_amp_gain)
    plt.savefig('input_fft_amp_gain.png')
    plt.close()

#    print(freq.shape, data_fft.real.shape, data_fft.imag.shape)
    pd.DataFrame(np.vstack((freq, data_fft.real, data_fft.imag)).transpose()).to_csv('input_fft.csv', header=False, index=False)

    # --- LPF ---
    data_lpf = filter(data, args.fs, args.freq_pass, args.freq_stop, args.gain_pass, args.gain_stop, args.filter_type)
    freq, data_fft = fft(t, data_lpf)
    plt.figure()
    plt.plot(t, data_lpf)
    plt.savefig('lpf.png')
    plt.close()

#    print(data_fft)

    plt.figure()
    plt.plot(freq, data_fft.real)
    plt.savefig('lpf_fft_real.png')
    plt.close()

    data_fft_amp = np.sqrt(np.power(data_fft.real, 2) + np.power(data_fft.imag, 2))
    plt.figure()
    plt.plot(freq, data_fft_amp)
    plt.savefig('lpf_fft_amp.png')
    plt.close()

    data_fft_amp_gain = 20 * np.log10(data_fft_amp)
    plt.figure()
    plt.plot(freq, data_fft_amp_gain)
    plt.savefig('lpf_fft_amp_gain.png')
    plt.close()

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


