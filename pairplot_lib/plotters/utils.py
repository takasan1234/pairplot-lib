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


def regress_func(x, y, **kws):
    """
    回帰直線を描画する関数
    散図に回帰直線を追加
    
    Args:
        x: x軸のデータ
        y: y軸のデータ
        **kws: その他のキーワード引数
    """
    mask = ~np.logical_or(np.isnan(x), np.isnan(y))
    x_clean, y_clean = x[mask], y[mask]
    
    # データの長さをチェック
    if len(x_clean) < 2 or len(y_clean) < 2:
        return
    
    try:
        # 線形回帰を計算
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
        
        # 回帰直線を描画（黒色）
        ax = plt.gca()
        x_line = np.array([x_clean.min(), x_clean.max()])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, 'k-', linewidth=2, alpha=0.8)
    except (ValueError, RuntimeError):
        # 回帰計算でエラーが発生した場合は何もしない
        pass
