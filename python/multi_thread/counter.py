#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import sys
import time
import argparse

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='10秒をカウントするサンプルプログラム\n'
                ' * カウント時，一定間隔で標準エラー出力する\n'
                ' * 間隔は引数--intervalで指定する(default=1[sec])',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--interval', dest='interval', type=float, default=1.0, required=False, \
            help='標準エラー出力する間隔')
    parser.add_argument('--thread_id', dest='thread_id', type=int, default=0, required=True, \
            help='multi_thread.pyから呼び出す際のスレッドID')

    args = parser.parse_args()

    return args

def counter(interval, thread_id):
    start = time.time()
    end = start
    while ((end - start) <= 10):
        time.sleep(interval)
        end = time.time()
        sys.stderr.write('[INFO][TH:{}] elapsed time : {}\n'.format(thread_id, end-start))
    
    return

def main():
    # --- 引数処理 ---
    args = ArgParser()

    # --- カウント ---
    counter(args.interval, args.thread_id)

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


