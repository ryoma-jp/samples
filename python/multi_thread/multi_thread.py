#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import threading
import concurrent.futures
import argparse
import subprocess
import counter

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='マルチスレッドのサンプルプログラム',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--n_thread', dest='n_thread', type=int, default=3, required=True, \
            help='作成するスレッド数')
    parser.add_argument('--use_subprocess', dest='use_subprocess', action='store_true', required=False, \
            help='subprocessを使用する場合にセット')

    args = parser.parse_args()

    return args

def thread_func(interval, use_subprocess=False):

    # --- スレッドIDを取得 ---
    thread_id = threading.get_ident()

    # --- カウント開始 ---
    if (use_subprocess):
        command = 'python3 counter.py --thread_id {} --interval {} 2>&1 | tee log_th{}.txt'.format(\
                    thread_id, interval, thread_id)
        subprocess.run(command, shell=True)
    else:
        counter.counter(interval, thread_id)

    return

def main():
    # --- 引数処理 ---
    args = ArgParser()

    # --- マルチスレッド処理 ---
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=args.n_thread)
    for i in range(args.n_thread):
        interval = 2.0 / (i+1)
        executor.submit(thread_func, interval, args.use_subprocess)

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


