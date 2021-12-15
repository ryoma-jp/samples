""" Evaluate
"""

import tensorflow as tf
from .masking import create_masks

def evaluate(model, inp_sentence, tokenizer_pt, tokenizer_en, max_length=40):
	start_token = [tokenizer_pt.vocab_size]
	end_token = [tokenizer_pt.vocab_size + 1]

	# inp文はポルトガル語、開始および終了トークンを追加
	inp_sentence = start_token + tokenizer_pt.encode(inp_sentence) + end_token
	encoder_input = tf.expand_dims(inp_sentence, 0)

	# ターゲットは英語であるため、Transformerに与える最初の単語は英語の
	# 開始トークンとなる
	decoder_input = [tokenizer_en.vocab_size]
	output = tf.expand_dims(decoder_input, 0)

	for i in range(max_length):
		enc_padding_mask, combined_mask, dec_padding_mask = create_masks(
			encoder_input, output)

		# predictions.shape == (batch_size, seq_len, vocab_size)
		predictions, attention_weights = model(encoder_input, 
													output,
													False,
													enc_padding_mask,
													combined_mask,
													dec_padding_mask)

		# seq_len次元から最後の単語を選択
		predictions = predictions[: ,-1:, :]  # (batch_size, 1, vocab_size)

		predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

		# predicted_idが終了トークンと等しいなら結果を返す
		if predicted_id == tokenizer_en.vocab_size+1:
			return tf.squeeze(output, axis=0), attention_weights

		# 出力にpredicted_idを結合し、デコーダーへの入力とする
		output = tf.concat([output, predicted_id], axis=-1)

	return tf.squeeze(output, axis=0), attention_weights


def translate(model, tokenizer_pt, tokenizer_en, sentence, max_length=40, plot=''):
	result, attention_weights = evaluate(model, sentence, tokenizer_pt, tokenizer_en, max_length=max_length)

	predicted_sentence = tokenizer_en.decode([i for i in result 
												if i < tokenizer_en.vocab_size])

	print('Input: {}'.format(sentence))
	print('Predicted translation: {}'.format(predicted_sentence))

	return predicted_sentence, attention_weights, result
