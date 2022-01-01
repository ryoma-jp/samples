#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import pickle
import pathlib
import logging

#---------------------------------
# 定数定義
#---------------------------------
BASE_DIR = '/tmp/subproc'
FIFO_NAME = 'fifo'
SUBPROC_LIST = f'{BASE_DIR}/subproc_list.pkl'

#---------------------------------
# 関数
#---------------------------------
def main():
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


