#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import pickle
import pathlib
import logging
import argparse
import time
import fcntl

#---------------------------------
# 定数定義
#---------------------------------
BASE_DIR = '/tmp/subproc'
FIFO_NAME = 'fifo'
SUBPROC_LIST = f'{BASE_DIR}/subproc_list.pkl'

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='ワーカプロセス',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--non-blocking', dest='non_blocking', action='store_true', required=False, \
            help='FIFOをノンブロッキングで読み込む(1[sec]毎のポーリング)')
    
    args = parser.parse_args()

    return args

def main():
    # --- 引数確認 ---
    args = ArgParser()
    print('args.non_blocking : {}'.format(args.non_blocking))
    
    # --- ハッシュリスト確認 ---
    if (pathlib.Path(SUBPROC_LIST).exists()):
        with open(SUBPROC_LIST, 'rb') as f:
            subproc_list = pickle.load(f)
    else:
        return
    sub_proc_dir = f'{BASE_DIR}/{subproc_list[os.getpid()]}'
    
    # --- FIFOファイルの取得 ---
    fifo = f'{sub_proc_dir}/{FIFO_NAME}'
    
    # --- ログのハンドラ設定 ---
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    log_dir = f'{sub_proc_dir}/log'
    os.makedirs(log_dir, exist_ok=True)
    handler = logging.FileHandler(filename=f'{log_dir}/log.txt')
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))
    logger.addHandler(handler)
    
    # --- コマンドループ ---
    while (True):
        if (args.non_blocking):
            time.sleep(1)       # 1[sec]毎にポーリング
            
            # --- ノンブロッキングでFIFOをオープン ---
            #  * 組み込み関数のopen()にはノンブロッキングでオープンするAPIがない
            #  * LowLevelの操作が可能なos.open()を使用してflagsにos.O_NONBLOCKを指定すると
            #    fifoをオープンする際にブロックされない
            #  * os.read()ではファイルディスクリプタに対してブロックが行われるようで，
            #    os.O_NONBLOCKフラグを外しておく
            #    ※os.O_NONBLOCKフラグを外さずにox.read()をコールすると例外BlockingIOErrorが発生する
            fd = os.open(fifo, os.O_RDONLY | os.O_NONBLOCK)
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            flags &= ~os.O_NONBLOCK
            fcntl.fcntl(fd, fcntl.F_SETFL, flags)
            
            try:
                # --- コマンドを取得 ---
                #  * os.read()ではbytes形でコマンドが取得される為，bytes.decode()でstr型を得る
                command = os.read(fd, 128)
                command = command.decode()[:-1]
                while (True):
                    buf = os.read(fd, 65536)
                    if not buf:
                        break
            finally:
                os.close(fd)
            
            if (command):
                logger.info(command)
            else:
                logger.info('FIFO is empty')
            
        else:
            with open(fifo, 'r') as f:
                command = f.readline()[:-1]
                logger.info(command)
            
        if (command == 'exit'):
            break
    
    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


