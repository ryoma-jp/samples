#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import tqdm
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA

#---------------------------------
# 定数定義
#---------------------------------
COLOR_LIST = ['red', 'blue', 'g', 'm', 'purple', 'aqua', 'gold', 'orange', 'cyan', 'indigo', 'crimson']

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='PCAによる次元圧縮のサンプルプログラム',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--data_type', dest='data_type', type=str, default='iris', required=False, \
            help='次元圧縮対象のデータ\n'
                 ' * \'iris\' : アヤメの計測データ\n'
                 ' * \'digits\' : 手書き数字データ\n')
    parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=True, \
            help='次元圧縮結果の保存ディレクトリ')

    args = parser.parse_args()

    return args

def draw_line_graph_with_bar(xdata, ydata_line, ydata_bar, xlabel='x', ylabel1='y1', ylabel2='y2', sample_labels_line=None, sample_labels_bar=None, output_dir=None, use_gui=False):
    # --- グラフ描画準備：第一軸(折れ線グラフ)，第二軸(棒グラフ) ---
    fig, ax1 = plt.subplots()   # ax1 : 第一軸(折れ線グラフ)
    ax2 = ax1.twinx()           # ax2 : 第二軸(棒グラフ)
    color_idx = 0
    xdata_idx = np.arange(len(xdata))
    
    if (sample_labels_line is None):
        sample_labels_line = ['line_data{}'.format(i) for i in range(len(ydata_line))]
    if (sample_labels_bar is None):
        sample_labels_bar = ['bar_data{}'.format(i) for i in range(len(ydata_bar))]

    # --- 第一軸を描画 ---
    for cnt, _ydata in enumerate(ydata_line):
        ax1.plot(xdata_idx, _ydata, marker='o', color=COLOR_LIST[color_idx % len(COLOR_LIST)], label=sample_labels_line[cnt])
        color_idx += 1
    
    # -- 第二軸を描画 ---
    bar_width = 0.8 / len(ydata_bar)
    for cnt, _ydata in enumerate(ydata_bar):
        ax2.bar(xdata_idx+bar_width*cnt, _ydata, width=bar_width, align='center', color=COLOR_LIST[color_idx % len(COLOR_LIST)], label=sample_labels_bar[cnt])
        color_idx += 1
    
    # --- 重ね順を設定 ---
    #   折れ線グラフを前面
    ax1.set_zorder(2)
    ax2.set_zorder(1)
    
    # --- 折れ線グラフの背景を透明に設定 ---
    ax1.patch.set_alpha(0)
    
    # --- ラベル，凡例設定 ---
    plt.xticks(xdata_idx+bar_width*0.5*(len(ydata_bar)-1), xdata)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel1)
    ax2.set_ylabel(ylabel2)
    ax1.set_ylim(0.0, 1.0)
    ax2.set_ylim(0.0, 1.0)
    ax1.legend(bbox_to_anchor=(0, 1), loc='upper left')
    ax2.legend(bbox_to_anchor=(0, 1.0-0.07*len(ydata_line)), loc='upper left')  # 暫定
    plt.tight_layout()
    
    # --- 保存・表示 ---
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'ev_ratio.png'))
    if (use_gui):
        plt.show()
    plt.close()
    
    return

def main():
    # --- 引数処理 ---
    args = ArgParser()
    
    # --- 出力ディレクトリ生成 ---
    os.makedirs(args.output_dir, exist_ok=True)
    
    # --- データセット取得 ---
    if (args.data_type == 'iris'):
        iris = datasets.load_iris()
        data = iris.data
        target = iris.target
        target_names = iris.target_names
    elif (args.data_type == 'digits'):
        digits = datasets.load_digits()
        data = digits.data
        target = digits.target
        target_names = digits.target_names
    else:
        print('[ERROR] Unknown data set : {}'.format(args.data_type))
        quit()
    
    print('[INFO] data type : {}'.format(args.data_type))
    print('[INFO] data.shape : {}'.format(data.shape))
    print('[INFO] target.shape : {}'.format(target.shape))
    print('[INFO] target_names : {}'.format(target_names))

    # --- 主成分分析 ---
    data_pca = PCA(random_state=0).fit(data.T)
    ev_ratio = data_pca.explained_variance_ratio_
    print('[INFO] components :\n{}'.format(data_pca.components_))
    print('[INFO] mean :\n{}'.format(data_pca.mean_))
    print('[INFO] covariance :\n{}'.format(data_pca.get_covariance()))
    print('[INFO] explained variance ratio :\n{}\n{}'.format(ev_ratio, ev_ratio.cumsum()))

    # --- 第二主成分までを散布図にプロット ---
    plt.figure()
    x = data_pca.components_[0]  # 第一主成分
    y = data_pca.components_[1]  # 第二主成分
    for i in range(len(target_names)):
        plt.scatter(x[target==i], y[target==i], label=target_names[i])
    plt.xlabel('1st component')
    plt.ylabel('2nd component')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(args.output_dir, 'pca.png'))
    plt.close()
    
    # --- 寄与率，累積寄与率をプロット ---
    x = ['component{}'.format(i) for i in range(len(data_pca.components_))]
    draw_line_graph_with_bar(x, ev_ratio.cumsum().reshape(1, -1), ev_ratio.reshape(1, -1), \
        xlabel='components', ylabel1='explained variance ratio(sum)', ylabel2='explained variance ratio', \
        sample_labels_line=['explained variance ratio(sum)'], sample_labels_bar=['explained variance ratio'], \
        output_dir=args.output_dir)
    
    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


