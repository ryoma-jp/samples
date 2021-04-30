/**
 * @file main.cpp
 * @brief TensorFlow LiteのC++ API利用サンプル
 */

#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"

/**
 * @struct tImgParams
 * @brief 画像データパラメータ
 */
typedef struct _tImgData {
	unsigned int height;
	unsigned int width;
	unsigned int channel;
	unsigned char* data;
} tImgData;

/**
 * @brief byteデータファイルを読み込む
 * @return int 0固定
 * @details byteデータファイルを読み込む
 */
static int load_bin_file(char* byte_file, tImgData* dst)
{
	FILE* fpByteFile;
	unsigned int read_data;
	unsigned int n_data;
	unsigned int d_type;
	float f_val;
	int i;

	/* --- file open --- */
	fpByteFile = fopen(byte_file, "rb");
	
	/* --- load n_data --- */
	fread(&n_data, 4, 1, fpByteFile);
	
	/* --- load d_type --- */
	fread(&d_type, 4, 1, fpByteFile);
	
	/* --- load data --- */
	if (d_type == 0) {
		/* --- Image Data --- */
		dst->data = (unsigned char*)malloc(n_data * sizeof(float));
		
		fread(&(dst->height), 4, 1, fpByteFile);
		fread(&(dst->width), 4, 1, fpByteFile);
		fread(&(dst->channel), 4, 1, fpByteFile);
		
		for (i = 0; i < n_data; i++) {
			fread(&read_data, 4, 1, fpByteFile);
			memcpy(dst->data + (i << 2), &read_data, 4);
		}
	} else {
		/* --- T.B.D --- */
	}
	
	fclose(fpByteFile);

	return 0;
}

/**
 * @brief プログラムの使用方法の表示
 * @return int 0固定
 * @details プログラムの使用方法を表示する
 */
static int show_usage()
{
	printf("<< Usage >>\n");
	printf("  TensorFlow LiteのC++ API利用サンプル\n");
	printf("  ./tflite_inference <tflite_file> <input_file>\n");
	printf("    tflite_file: TensorFlow Liteファイル\n");
	printf("    input_file: 入力データファイル\n");

	return 0;
}

/**
 * @brief メイン関数
 * @param[in] argc 引数の数
 * @param[in] argv 引数
 * @return int 0固定
 * @details TensorFlow LiteのC++ API利用サンプル
 */
int main(int argc, char* argv[])
{
	/* --- 変数宣言 --- */
	char* tflite_file;
	char* input_file;
	
	/* --- 引数取り込み --- */
	if (argc != 3) {
		show_usage();
		exit(0);
	} else {
		tflite_file = argv[1];
		input_file = argv[2];
	}
	
	/* --- tfliteファイル読み込み --- */
	std::unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile(tflite_file);
	
	/* --- インタプリタ構築 --- */
	tflite::ops::builtin::BuiltinOpResolver resolver;
	std::unique_ptr<tflite::Interpreter> interpreter;
	tflite::InterpreterBuilder(*model, resolver)(&interpreter);
	
	/* --- Tensor Buffer確保 --- */
	interpreter->AllocateTensors();
	
	/* --- 入力データをセット --- */
	tImgData image_data;
	float* input = interpreter->typed_input_tensor<float>(0);
	load_bin_file(input_file, &image_data);
	
	int data_len = image_data.height * image_data.width * image_data.channel * sizeof(float);
	memcpy(input, image_data.data, data_len);
	
	/* --- 推論実行 --- */
	interpreter->Invoke();

	float* output = interpreter->typed_output_tensor<float>(0);
	printf("[OUTPUT]\n");
	for (int o = 0; o < 10; o++) {
		printf("  * [%d] %e\n", o, output[o]);
	}
	
	return 0;
}

