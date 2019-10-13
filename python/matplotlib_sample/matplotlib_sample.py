#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import io
import os
import tqdm
import argparse
import pandas as pd
import numpy as np

#import matplotlib      #GUIのない環境で動かす場合にコメントアウトを外す
#matplotlib.use('Agg')  #GUIのない環境で動かす場合にコメントアウトを外す
import matplotlib.pyplot as plt

#---------------------------------
# 定数定義
#---------------------------------
COLOR_LIST = ['red', 'blue', 'g', 'm', 'purple', 'aqua', 'gold', 'orange', 'cyan', 'indigo', 'crimson']

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='matplotlibを用いたグラフ描画のサンプル',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--graph_type', dest='graph_type', type=str, default=None, required=True, \
            help='描画するグラフの種類(カンマ区切りで複数選択可)\n'
                 '  * \'line\' : 折れ線グラフ\n'
                 '  * \'bar\' : 棒グラフ\n'
                 '  * \'mixed_line_bar\' : 折れ線グラフと棒グラフの混合\n'
                 '  * \'x_log_10\' : 方対数グラフ(x軸)\n'
                 '  * \'y_log_10\' : 片対数グラフ(y軸)\n'
                 '  * \'xy_log_10\' : 両対数グラフ\n'
                 '  * \'heatmap\' : ヒートマップ\n'
                 '  * \'scatter\' : 散布図\n')
    parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=True, \
            help='描画したグラフの出力先ディレクトリ(存在しない場合は生成する)')
    parser.add_argument('--use_gui', dest='use_gui', action='store_true', required=False, \
            help='GUIを使う(pyplot.show()でのウィンドウ表示する)場合にセット')

    args = parser.parse_args()

    return args

def draw_line_graph(xdata, ydata, xlabel='x', ylabel='y', sample_labels=None, output_dir=None, use_gui=False):
    # --- グラフ描画準備 ---
    plt.figure()
    if (sample_labels is None):
        sample_labels = ['data{}'.format(i) for i in range(len(ydata))]
    
    # --- 折れ線グラフ描画 ---
    for cnt, _ydata in enumerate(ydata):
        plt.plot(xdata, _ydata, label=sample_labels[cnt])
    
    # --- ラベル，凡例設定 ---
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    
    # --- 保存・表示 ---
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'line.png'))
    if (use_gui):
        plt.show()
    plt.close()

    return

def draw_bar_graph(xdata, ydata, xlabel='x', ylabel='y', sample_labels=None, output_dir=None, use_gui=False):
    # --- グラフ描画準備 ---
    plt.figure()
    xdata_idx = np.arange(len(xdata))
    if (sample_labels is None):
        sample_labels = ['data{}'.format(i) for i in range(len(ydata))]
    bar_width = 0.8 / len(ydata)    # 0.8=default
    
    # --- 棒グラフ描画 ---
    for cnt, _ydata in enumerate(ydata):
        plt.bar(xdata_idx+bar_width*cnt, _ydata, width=bar_width, align='center', label=sample_labels[cnt])
    
    # --- ラベル，凡例設定 ---
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(xdata_idx+bar_width*0.5*(len(ydata)-1), xdata)
    plt.legend()
    plt.tight_layout()
    
    # --- 保存・表示 ---
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'bar.png'))
    if (use_gui):
        plt.show()
    plt.close()
    
    return

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
    ax1.legend(bbox_to_anchor=(0, 1), loc='upper left')
    ax2.legend(bbox_to_anchor=(0, 1.0-0.07*len(ydata_line)), loc='upper left')  # 暫定
    plt.tight_layout()
    
    # --- 保存・表示 ---
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'line_bar.png'))
    if (use_gui):
        plt.show()
    plt.close()
    
    return

def draw_scatter_graph(xdata, ydata, xlabel='x', ylabel='y', sample_labels=None, output_dir=None, use_gui=False):
    # --- グラフ描画準備 ---
    plt.figure()
    if (sample_labels is None):
        sample_labels = ['data{}'.format(i) for i in range(len(xdata))]
    
    # --- 散布図描画 ---
    for cnt, (_xdata, _ydata) in enumerate(zip(xdata, ydata)):
        plt.scatter(_xdata, _ydata, label=sample_labels[cnt])
    
    # --- ラベル，凡例設定 ---
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    
    # --- 保存・表示 ---
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'scatter.png'))
    if (use_gui):
        plt.show()
    plt.close()
    
    return

def main():
    # --- 引数処理 ---
    args = ArgParser()
    list_graph_type = pd.read_csv(io.StringIO(args.graph_type), header=None, skipinitialspace=True).values[0]

    # --- 出力ディレクトリ生成 ---
    os.makedirs(args.output_dir, exist_ok=True)

    # --- グラフを描画 ---
    for cnt, graph_type in enumerate(tqdm.tqdm(list_graph_type)):
        print('[INFO] Draw graph #{} : {}'.format(cnt+1, graph_type))

        if (graph_type == 'line'):
            # --- 入力データ作成 ---
            n_samples = 51
            n_data = 3
            x = np.linspace(-3, 3, n_samples)
            y_tmp = np.random.rand(n_samples) * 3
            y = np.array([y_tmp / (i+1) for i in range(n_data)])
            
            # --- グラフ描画 ---
            draw_line_graph(x, y, output_dir=args.output_dir, use_gui=args.use_gui)
        elif (graph_type == 'bar'):
            # --- 入力データ生成 ---
            x = ['x0', 'x1', 'x2', 'x3', 'x4']
#            y = np.array([[100, 200, 300, 400, 500]])
            y = np.array([[100, 200, 300, 400, 500], [150, 250, 350, 450, 550]])
#            y = np.array([[100, 200, 300, 400, 500], [150, 250, 350, 450, 550], [50, 150, 250, 350, 450]])
#            y = np.array([[100, 200, 300, 400, 500], [150, 250, 350, 450, 550], [50, 150, 250, 350, 450], [200, 300, 400, 500, 600]])
            
            # --- グラフ描画 ---
            draw_bar_graph(x, y, output_dir=args.output_dir, use_gui=args.use_gui)
        elif (graph_type == 'mixed_line_bar'):
            # --- 入力データ生成 ---
            x = ['x0', 'x1', 'x2', 'x3', 'x4']
            y_line = np.array([[100, 200, 300, 400, 500]])    # 折れ線グラフ用データ
            y_bar = np.array([[150, 250, 350, 450, 550]])     # 棒グラフ用データ
            
            # --- グラフ描画 ---
            draw_line_graph_with_bar(x, y_line, y_bar, output_dir=args.output_dir, use_gui=args.use_gui)
        elif (graph_type == 'scatter'):
            # --- 入力データ生成 ---
            xdata = np.random.rand(2, 10)
            ydata = np.random.rand(2, 10)
            
            # --- グラフ描画 ---
            draw_scatter_graph(xdata, ydata, output_dir=args.output_dir, use_gui=args.use_gui)
        else:
            print('[ERROR] Unknown graph type : {}'.format(graph_type))

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


