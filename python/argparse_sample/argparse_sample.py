#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import io
import pandas as pd
import argparse

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='argparseモジュールのサンプルプログラム',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--string', dest='string', type=str, default=None, required=False, \
            help='文字列引数')
    parser.add_argument('--int', dest='int', type=int, default=None, required=False, \
            help='整数引数')
    parser.add_argument('--float', dest='float', type=float, default=None, required=False, \
            help='浮動小数引数')
    parser.add_argument('--bool', dest='bool', action='store_true', required=False, \
            help='BOOL引数')

    args = parser.parse_args()

    return args

def main():
    # --- 引数処理 ---
    args = ArgParser()
    print('args.string : {}'.format(args.string))
    print('args.int : {}'.format(args.int))
    print('args.float : {}'.format(args.float))
    print('args.bool : {}'.format(args.bool))

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


