"""Metrics

メトリクス計算用モジュール
"""

from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

class CalcMetrics():
    """CalcMetrics

    メトリクス計算クラス

    Attributes:
        mae: Mean Average Error
        mse: Mean Squared Error
        r2_score: R2 Score
    """

    def __init__(self, pred, target):
        """__init__

        メトリクス算出し，メンバ変数へ登録する

        Args:
            pred(numpy.ndarray): 推定結果
            target(numpy.ndarray, pandas.DataFrame): 正解
        """

        self.mae = mean_absolute_error(target, pred)
        self.mse = mean_squared_error(target, pred)
        self.r2_score = r2_score(target, pred)

