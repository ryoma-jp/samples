#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import pathlib
import argparse
import time
import subprocess
import hashlib
import pickle
import json

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
    parser = argparse.ArgumentParser(description='ワーカプロセスをFIFOを介して制御するプロセス間通信サンプル',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--command', dest='command', type=str, default=None, required=False, \
            help='ワーカプロセス制御コマンド\n'
                 '  * open: ワーカプロセスを起動する\n'
                 '  * exit: ワーカプロセスを終了する\n'
                 '          --pidによるPID指定が必要\n')
    parser.add_argument('--pid', dest='pid', type=int, default=None, required=False, \
            help='制御対象のプロセスIDを指定する')
    parser.add_argument('--list', dest='list', action='store_true', required=False, \
            help='ワーカプロセスの一覧を表示する\n'
                 '本フラグが設定された場合は--commandは無視する')
    parser.add_argument('--non-blocking', dest='non_blocking', action='store_true', required=False, \
            help='ワーカプロセスがFIFOをノンブロッキングで読み込む(1[sec]毎のポーリング)')
    
    args = parser.parse_args()

    return args

def main():
    def _get_subproc_list(pkl_subproc_list):
        if (pathlib.Path(pkl_subproc_list).exists()):
            with open(pkl_subproc_list, 'rb') as f:
                subproc_list = pickle.load(f)
        else:
            subproc_list = None
        
        return subproc_list
    
    def _dump_subproc_list(pkl_subproc_list, subproc_list):
        with open(pkl_subproc_list, 'wb') as f:
            pickle.dump(subproc_list, f)
        return
    
    # --- 引数処理 ---
    args = ArgParser()
    print('args.command : {}'.format(args.command))
    print('args.pid : {}'.format(args.command))
    print('args.list : {}'.format(args.list))
    print('args.non_blocking : {}'.format(args.non_blocking))

    # --- ワーカ一覧表示 or コマンド送信 ---
    if (args.list):
        subproc_list = _get_subproc_list(SUBPROC_LIST)
        if (subproc_list is None):
            print(f'[ERROR] {SUBPROC_LIST} is not exist')
            return
        
        print(json.dumps(subproc_list, indent=4))
    else:
        # --- ワーカプロセス制御 ---
        if (args.command == 'open'):
            sub_proc_hash = hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()
            print(sub_proc_hash)
            
            subprocess.run(['mkdir', '-p', f'{BASE_DIR}/{sub_proc_hash}'])
            subprocess.run(['mkfifo', f'{BASE_DIR}/{sub_proc_hash}/{FIFO_NAME}'])
            if (args.non_blocking):
                sub_proc = subprocess.Popen(['python', 'sub_proc.py', '--non-blocking'])
            else:
                sub_proc = subprocess.Popen(['python', 'sub_proc.py'])
            
            subproc_list = _get_subproc_list(SUBPROC_LIST)
            if (subproc_list is None):
                subproc_list = {}
            subproc_list[sub_proc.pid] = sub_proc_hash
            print(subproc_list)
            _dump_subproc_list(SUBPROC_LIST, subproc_list)
            
        else:
            # --- サブプロセスリストを取得 ---
            subproc_list = _get_subproc_list(SUBPROC_LIST)
            if (subproc_list is None):
                print(f'[ERROR] {SUBPROC_LIST} is not exist')
                return
            
            # --- サブプロセスへコマンドを送信 ---
            if (args.pid in subproc_list.keys()):
                sub_proc_hash = subproc_list[args.pid]
                fifo = f'{BASE_DIR}/{sub_proc_hash}/{FIFO_NAME}'
                with open(fifo, 'w') as f:
                    f.write(f'{args.command}\n')
                
                if (args.command == 'exit'):
                    del subproc_list[args.pid]
                    _dump_subproc_list(SUBPROC_LIST, subproc_list)
            else:
                print(f'[ERROR] Key({args.pid}) is not found')
    
    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


