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


def corr_func_colored(x, y, **kws):
    """
    色分けペアプロット用の相関係数アノテーション関数
    全体のデータに対して相関係数を計算（色分けを無視）
    
    Args:
        x: x軸のデータ
        y: y軸のデータ
        **kws: その他のキーワード引数
    """
    # 色分けペアプロットでは、各サブプロットで同じ相関係数を表示するのを避けるため、
    # 最初のサブプロット（左上から右下への対角線上の最初の要素）でのみ表示
    ax = plt.gca()
    
    # 現在のサブプロットの位置を取得
    fig = ax.figure
    axes = fig.axes
    
    # 現在の軸が下三角部分の最初の要素かどうかをチェック
    current_ax_index = axes.index(ax)
    
    # 下三角部分の最初の要素でのみ相関係数を表示
    if current_ax_index == 0:  # 最初のサブプロット（左下）でのみ表示
        mask = ~np.logical_or(np.isnan(x), np.isnan(y))
        x_clean, y_clean = x[mask], y[mask]
        
        # データの長さをチェック
        if len(x_clean) < 2 or len(y_clean) < 2:
            ax.annotate("r = N/A",
                        xy=(.2, .5),
                        xycoords=ax.transAxes,
                        size=16)
            return
        
        try:
            r, _ = stats.pearsonr(x_clean, y_clean)
            ax.annotate("r = {:.3f}".format(r),
                        xy=(.2, .5),
                        xycoords=ax.transAxes,
                        size=16)
        except ValueError:
            # 相関係数計算でエラーが発生した場合
            ax.annotate("r = N/A",
                        xy=(.2, .5),
                        xycoords=ax.transAxes,
                        size=16)
