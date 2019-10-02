#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from modules.SubModule1 import SubModule1
from modules.SubModule2 import SubModule2

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def main():
    SubModule1.SubModule1()
    SubModule2.SubModule2()

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


