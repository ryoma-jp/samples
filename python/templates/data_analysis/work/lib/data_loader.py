"""Data Loader

データ読み込み用のモジュール
"""

def load_california_housing():
    """load_california_housing

    カリフォルニア住宅価格予測用データセットをロードする

    Returns:
        ロードしたデータセット

        - df_x(pandas.DataFrame): 入力データ
        - df_y(pandas.DataFrame): 出力データ
    """

    import pandas as pd
    from sklearn.datasets import fetch_california_housing
    
    california_housing = fetch_california_housing()
    df_x = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
    df_y = pd.DataFrame(california_housing.target, columns=['TARGET'])

    return df_x, df_y

def load_cifar10(dataset_dir):
    """load_cifar10

    CIFAR-10画像分類用データセットをロードする
    
    Args:
        dataset_dir (pathlib.Path): Pythonバージョン(https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz)の解凍先ディレクトリを指定する

    Returns:
        ロードしたデータセット

        - dict_x (dict):
            - 学習データ，テストデータの画像データをnumpy.ndarray形式で返す
            - フォーマット
                - keys: ['train', 'test']
                - image data shape: [NCHW]
            
        - dict_y (dict):
            - 学習データ，テストデータの正解ラベルを返す
            - 各正解ラベルのラベル名も'label_name'として返す
            - フォーマット
                - keys: ['train', 'test', 'label_names']
                - label data shape: [N]
                - label_name data shape: [10]
            
    """
    
    import numpy as np
    
    def _unpickle(file):
        import pickle
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict
    
    # --- load training data ---
    train_data_list = ["data_batch_1", "data_batch_2", "data_batch_3", "data_batch_4", "data_batch_5"]
    dict_data = _unpickle(dataset_dir.joinpath(train_data_list[0]))
    train_images = dict_data[b'data']
    train_labels = dict_data[b'labels'].copy()
    for train_data in train_data_list[1:]:
        dict_data = _unpickle(dataset_dir.joinpath(train_data))
        train_images = np.vstack((train_images, dict_data[b'data']))
        train_labels = np.hstack((train_labels, dict_data[b'labels']))
    
    # --- load test data ---
    test_data = "test_batch"
    dict_data = _unpickle(dataset_dir.joinpath(test_data))
    test_images = dict_data[b'data']
    test_labels = np.array(dict_data[b'labels'].copy())
    
    # --- transpose: [N, C, H, W] -> [N, H, W, C] ---
    train_images = train_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
    test_images = test_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
    
    # --- load label name ---
    meta_data = _unpickle(dataset_dir.joinpath('batches.meta'))
    label_data = [_x.decode('utf-8') for _x in meta_data[b'label_names']]
    
    dict_x = {'train': train_images, 'test': test_images}
    dict_y = {'train': train_labels, 'test': test_labels, 'label_names': label_data}
    return dict_x, dict_y
    