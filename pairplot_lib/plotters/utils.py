"""
ペアプロット用の共通ユーティリティ関数
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def corr_func(x, y, **kws):
    """
    カスタムの相関係数アノテーション関数
    散布図の下三角部分に相関係数を表示
    
    Args:
        x: x軸のデータ
        y: y軸のデータ
        **kws: その他のキーワード引数
    """
    mask = ~np.logical_or(np.isnan(x), np.isnan(y))
    x, y = x[mask], y[mask]
    
    # データの長さをチェック
    if len(x) < 2 or len(y) < 2:
        ax = plt.gca()
        ax.annotate("r = N/A",
                    xy=(.2, .5),
                    xycoords=ax.transAxes,
                    size=16)
        return
    
    try:
        r, _ = stats.pearsonr(x, y)
        ax = plt.gca()
        ax.annotate("r = {:.3f}".format(r),
                    xy=(.2, .5),
                    xycoords=ax.transAxes,
                    size=16)
    except ValueError:
        # 相関係数計算でエラーが発生した場合
        ax = plt.gca()
        ax.annotate("r = N/A",
                    xy=(.2, .5),
                    xycoords=ax.transAxes,
                    size=16)
