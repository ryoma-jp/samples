#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import cv2
import argparse

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
    parser = argparse.ArgumentParser(description='カメラ入力のサンプル',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    #  * なし

    args = parser.parse_args()

    return args

def main():
    # --- 引数処理 ---
    args = ArgParser()

    # --- カメラ映像取得処理 ---
    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        cv2.imshow('title', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()

    return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
    main()


