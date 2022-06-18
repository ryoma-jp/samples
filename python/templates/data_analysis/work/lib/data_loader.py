"""Data Loader

データ読み込み用のモジュール
"""

from sklearn.datasets import fetch_california_housing
import pandas as pd

def load_dataset():
    """load_dataset

    データセットをロードする

    Returns:
        df_x(pandas.DataFrame): 入力データ
        df_y(pandas.DataFrame): 出力データ
    """

    california_housing = fetch_california_housing()
    df_x = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
    df_y = pd.DataFrame(california_housing.target, columns=['TARGET'])

    return df_x, df_y
