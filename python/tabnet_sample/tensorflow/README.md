# TabNetのサンプル

## 概要

* TabNetのTensorFlowサンプル

## 実行手順

	$ cd docker  
	$ docker build -t tabnet/tensorflow:21.03-tf2-py3 .  
	$ ./docker_run.sh  
	# cd /work  
	# ./run.sh  

実行は可能だが，下記エラーが発生して中断される．
WSL2では実行不可か？

	Traceback (most recent call last):
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/client/session.py", line 1365, in _do_call
	    return fn(*args)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/client/session.py", line 1349, in _run_fn
	    return self._call_tf_sessionrun(options, feed_dict, fetch_list,
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/client/session.py", line 1441, in _call_tf_sessionrun
	    return tf_session.TF_SessionRun_wrapper(self._session, options, feed_dict,
	tensorflow.python.framework.errors_impl.InternalError: 2 root error(s) found.
	  (0) Internal: cuDNN launch failure : input shape ([116203,1,1,54])
		 [[{{node Encoder_2/batch_normalization/FusedBatchNormV3}}]]
	  (1) Internal: cuDNN launch failure : input shape ([116203,1,1,54])
		 [[{{node Encoder_2/batch_normalization/FusedBatchNormV3}}]]
		 [[Encoder_1/input_layer/Soil_Type28_embedding/Soil_Type28_embedding_weights/Cast/x/_4537]]
	0 successful operations.
	0 derived errors ignored.

	During handling of the above exception, another exception occurred:

	Traceback (most recent call last):
	  File "experiment_covertype.py", line 200, in <module>
	    app.run(main)
	  File "/usr/local/lib/python3.8/dist-packages/absl/app.py", line 303, in run
	    _run_main(main, args)
	  File "/usr/local/lib/python3.8/dist-packages/absl/app.py", line 251, in _run_main
	    sys.exit(main(argv))
	  File "experiment_covertype.py", line 172, in main
	    _, train_loss, merged_summary = sess.run(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/client/session.py", line 955, in run
	    result = self._run(None, fetches, feed_dict, options_ptr,
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/client/session.py", line 1179, in _run
	    results = self._do_run(handle, final_targets, final_fetches,
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/client/session.py", line 1358, in _do_run
	    return self._do_call(_run_fn, feeds, fetches, targets, options,
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/client/session.py", line 1384, in _do_call
	    raise type(e)(node_def, op, message)
	tensorflow.python.framework.errors_impl.InternalError: 2 root error(s) found.
	  (0) Internal: cuDNN launch failure : input shape ([116203,1,1,54])
		 [[node Encoder_2/batch_normalization/FusedBatchNormV3 (defined at /usr/local/lib/python3.8/dist-packages/tensorflow_core/python/framework/ops.py:1748) ]]
	  (1) Internal: cuDNN launch failure : input shape ([116203,1,1,54])
		 [[node Encoder_2/batch_normalization/FusedBatchNormV3 (defined at /usr/local/lib/python3.8/dist-packages/tensorflow_core/python/framework/ops.py:1748) ]]
		 [[Encoder_1/input_layer/Soil_Type28_embedding/Soil_Type28_embedding_weights/Cast/x/_4537]]
	0 successful operations.
	0 derived errors ignored.

	Original stack trace for 'Encoder_2/batch_normalization/FusedBatchNormV3':
	  File "experiment_covertype.py", line 200, in <module>
	    app.run(main)
	  File "/usr/local/lib/python3.8/dist-packages/absl/app.py", line 303, in run
	    _run_main(main, args)
	  File "/usr/local/lib/python3.8/dist-packages/absl/app.py", line 251, in _run_main
	    sys.exit(main(argv))
	  File "experiment_covertype.py", line 141, in main
	    encoded_test_batch, _ = tabnet_forest_covertype.encoder(
	  File "/work/google-research/tabnet/tabnet_model.py", line 92, in encoder
	    features = tf.layers.batch_normalization(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/util/deprecation.py", line 330, in new_func
	    return func(*args, **kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/layers/normalization.py", line 327, in batch_normalization
	    return layer.apply(inputs, training=training)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/util/deprecation.py", line 330, in new_func
	    return func(*args, **kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/keras/engine/base_layer.py", line 1700, in apply
	    return self.__call__(inputs, *args, **kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/layers/base.py", line 548, in __call__
	    outputs = super(Layer, self).__call__(inputs, *args, **kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/keras/engine/base_layer.py", line 854, in __call__
	    outputs = call_fn(cast_inputs, *args, **kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/autograph/impl/api.py", line 234, in wrapper
	    return converted_call(f, options, args, kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/autograph/impl/api.py", line 439, in converted_call
	    return _call_unconverted(f, args, kwargs, options)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/autograph/impl/api.py", line 330, in _call_unconverted
	    return f(*args, **kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/layers/normalization.py", line 167, in call
	    return super(BatchNormalization, self).call(inputs, training=training)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/keras/layers/normalization.py", line 710, in call
	    outputs = self._fused_batch_norm(inputs, training=training)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/keras/layers/normalization.py", line 564, in _fused_batch_norm
	    output, mean, variance = tf_utils.smart_cond(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/keras/utils/tf_utils.py", line 58, in smart_cond
	    return smart_module.smart_cond(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/framework/smart_cond.py", line 56, in smart_cond
	    return false_fn()
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/keras/layers/normalization.py", line 554, in _fused_batch_norm_inference
	    return nn.fused_batch_norm(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/ops/nn_impl.py", line 1493, in fused_batch_norm
	    y, batch_mean, batch_var, _, _, _ = gen_nn_ops.fused_batch_norm_v3(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/ops/gen_nn_ops.py", line 4616, in fused_batch_norm_v3
	    _, _, _op = _op_def_lib._apply_op_helper(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/framework/op_def_library.py", line 792, in _apply_op_helper
	    op = g.create_op(op_type_name, inputs, dtypes=None, name=scope,
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/util/deprecation.py", line 513, in new_func
	    return func(*args, **kwargs)
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/framework/ops.py", line 3356, in create_op
	    return self._create_op_internal(op_type, inputs, dtypes, input_types, name,
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/framework/ops.py", line 3418, in _create_op_internal
	    ret = Operation(
	  File "/usr/local/lib/python3.8/dist-packages/tensorflow_core/python/framework/ops.py", line 1748, in __init__
	    self._traceback = tf_stack.extract_stack()


## 参考

* [google-research/tabnet/](https://github.com/google-research/google-research/tree/master/tabnet)


