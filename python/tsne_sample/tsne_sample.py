#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import tqdm
import argparse
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.manifold import TSNE

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='t-SNEによる次元圧縮のサンプルプログラム',
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

    for perplexity in tqdm.tqdm([5, 10, 20, 30, 40, 50]):
        data_tsne = TSNE(n_components=2, random_state=0, perplexity=perplexity).fit_transform(data)
        plt.figure()
        x = data_tsne[:, 0]
        y = data_tsne[:, 1]
        for i in range(len(target_names)):
            plt.scatter(x[target==i], y[target==i], label=target_names[i])
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(args.output_dir, 'tsne-perplexity{}.png'.format(perplexity)))
        plt.close()
    
    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


