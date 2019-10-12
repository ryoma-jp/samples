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
                 '  * \'scatter\' : 散布図\n')
    parser.add_argument('--output_dir', dest='output_dir', type=str, default=None, required=True, \
            help='描画したグラフの出力先ディレクトリ(存在しない場合は生成する)')
    parser.add_argument('--use_gui', dest='use_gui', action='store_true', required=False, \
            help='GUIを使う(pyplot.show()でのウィンドウ表示する)場合にセット')

    args = parser.parse_args()

    return args

def draw_line_graph(xdata, ydata, xlabel='x', ylabel='y', output_dir=None, use_gui=False):
    plt.figure()
    for _ydata in ydata:
        plt.plot(xdata, _ydata)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'line.png'))
    if (use_gui):
        plt.show()
    plt.close()

    return

def draw_bar_graph(ydata, xlabel=['x'], ylabel='y', output_dir=None, use_gui=False):
    plt.figure()
    xdata = np.arange(len(xlabel))
    bar_width = 0.8 / len(ydata)    # 0.8=default
    for cnt, _ydata in enumerate(ydata):
        plt.bar(xdata+bar_width*cnt, _ydata, width=bar_width, align='center')
    plt.ylabel(ylabel)
    plt.xticks(xdata+bar_width*(1.0-1.0/len(ydata)), xlabel)
    plt.tight_layout()
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'bar.png'))
    if (use_gui):
        plt.show()
    plt.close()
    
    return

def draw_line_graph_with_bar(xdata, ydata_line, ydata_bar, xlabel=['x'], ylabel1='y1', ylabel2='y2', output_dir=None, use_gui=False):
    # --- 第一軸(折れ線グラフ)と第二軸(棒グラフ)を定義 ---
    fig, ax1 = plt.subplots()   # ax1 : 第一軸(折れ線グラフ)
    ax2 = ax1.twinx()           # ax2 : 第二軸(棒グラフ)
    color_idx = 0
    
    # --- 第一軸をプロット ---
    for _ydata in ydata_line:
        plt.plot(xdata, _ydata, marker='o', color=COLOR_LIST[color_idx % len(COLOR_LIST)])
        color_idx += 1
    
    # -- 第二軸をプロット ---
    bar_width = 0.8 / len(ydata_bar)
    for cnt, _ydata in enumerate(ydata_bar):
        plt.bar(xdata+bar_width*cnt, _ydata, width=bar_width, align='center', color=COLOR_LIST[color_idx % len(COLOR_LIST)])
        color_idx += 1
    
    # --- 重ね順を設定 ---
    #   折れ線グラフを前面
    ax1.set_zorder(2)
    ax2.set_zorder(1)
    
    # --- 折れ線グラフの背景を透明に設定 ---
    ax1.patch.set_alpha(0)
    
    # --- ラベルを設定 ---
    plt.xticks(xdata+bar_width*(1.0-1.0/len(ydata_bar)), xlabel)
    ax1.set_ylabel(ylabel1)
    ax2.set_ylabel(ylabel2)
    
    # --- 保存・表示 ---
    if (output_dir is not None):
        plt.savefig(os.path.join(output_dir, 'line_bar.png'))
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
            y = np.array([[100, 200, 300, 400, 500], [150, 250, 350, 450, 550]])
            xlabel = ['x0', 'x1', 'x2', 'x3', 'x4']
            
            # --- グラフ描画 ---
            draw_bar_graph(y, xlabel=xlabel, output_dir=args.output_dir, use_gui=args.use_gui)
        elif (graph_type == 'mixed_line_bar'):
            # --- 入力データ生成 ---
            xlabel = ['x0', 'x1', 'x2', 'x3', 'x4']
            y_line = np.array([[100, 200, 300, 400, 500]])    # 折れ線グラフ用データ
            y_bar = np.array([[150, 250, 350, 450, 550]])     # 棒グラフ用データ
            
            # --- グラフ描画 ---
            draw_line_graph_with_bar(np.arange(len(xlabel)), y_line, y_bar, xlabel, output_dir=args.output_dir, use_gui=args.use_gui)
        elif (graph_type == 'scatter'):
            pass
        else:
            print('[ERROR] Unknown graph type : {}'.format(graph_type))

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


