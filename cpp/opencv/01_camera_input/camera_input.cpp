/*******************************************************
 * [ 説明 ]
 *  OpenCVを用いたカメラ入力処理のサンプル
 *******************************************************/

/*******************************************************
 * インクルードファイル
 *******************************************************/
#include "opencv2/opencv.hpp"
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

/*******************************************************
 * 定数定義
 *******************************************************/

/*******************************************************
 * 列挙体／構造体
 *******************************************************/

/*******************************************************
 * 関数宣言
 *******************************************************/

/*******************************************************
 * 変数宣言
 *******************************************************/

/**
 * @fn int main(int argc, char* argv[])
 * @brief カメラ入力処理のサンプル
 * @return 0固定
 */
using namespace cv;
int main(int argc, char *argv[])
{
	/* --- 変数宣言 --- */
	signed char key;
	Mat im, im_sobel, im_laplacian, im_canny, im_tmp;

	/* --- カメラのキャプチャ --- */
	VideoCapture cap(0);

	/* --- キャプチャできないときのエラー処理 --- */
	printf("Press key to exit\n");
	while (1) {
		/* --- カメラ映像取得 --- */
		cap >> im;

		/* --- Sobelフィルタでエッジ検出 --- */
		Sobel(im, im_tmp, CV_32F, 1, 1);
		convertScaleAbs(im_tmp, im_sobel, 1, 0);

		/* --- Laplacianフィルタでエッジ検出 --- */
		Laplacian(im, im_tmp, CV_32F, 3);
		convertScaleAbs(im_tmp, im_laplacian, 1, 0);   

		/* --- Cannyアルゴリズムでエッジ検出 --- */
		Canny(im, im_canny, 50, 200);

		/* --- 表示 --- */
		imshow("Camera", im);
		imshow("Sobel", im_sobel);
		imshow("Laplacian", im_laplacian);
		imshow("Canny", im_canny);

		/* --- キー入力があれば終了 --- */
		key = waitKey(33);
		if (key >= 0) {
			printf("key(%d) is Pressed", key);
			break;
		}
	}

	/* --- 終了 --- */
	return 0;
}
