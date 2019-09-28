#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import io
import pandas as pd

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def main():
    data = "read, csv, with, StringIO"
    df_data = pd.read_csv(io.StringIO(data), header=None, skipinitialspace=True)
    df_data.to_csv('out.csv', header=False, index=False)

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()

