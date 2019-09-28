#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import argparse
import subprocess

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='外部プログラムを呼び出すサンプルプログラム',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--bin', dest='bin', type=str, default=None, required=True, \
            help='実行する外部プログラムを引数含めて文字列で指定')

    args = parser.parse_args()
    return args

def main():
    # --- 引数処理 ---
    args = ArgParser()

    # --- 外部プログラム実行 ---
    result = subprocess.run(args.bin, shell=True)
    result = subprocess.run(args.bin, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('result.args={}, result.returncode={}, result.stdout={}, result.stderr={}'.format( \
            result.args, result.returncode, result.stdout, result.stderr))

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()

