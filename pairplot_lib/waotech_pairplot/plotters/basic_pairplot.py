"""
基本的なペアプロット（相関係数表示付き）
pairplot2.pyの機能を移植
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def corr_func(x, y, **kws):
    """
    カスタムの相関係数アノテーション関数
    散布図の下三角部分に相関係数を表示
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


def create_basic_pairplot(df: pd.DataFrame, numeric_cols: list, output_path: str) -> str:
    """
    基本的なペアプロット（相関係数表示付き）を作成
    
    Args:
        df: 入力DataFrame
        numeric_cols: プロットする数値列のリスト
        output_path: 出力ファイルパス
        
    Returns:
        保存したファイルパス
    """
    # 数値列が2列未満の場合は警告
    if len(numeric_cols) < 2:
        raise ValueError("エラー: 少なくとも2つの数値列が必要です。")
    
    # プロットするデータを選択
    plots = df[numeric_cols]
    
    # データ情報を表示
    print(f"利用可能な数値列: {numeric_cols}")
    print(f"データの形状: {df.shape}")
    print(f"数値データの形状: {plots.shape}")
    print(f"欠損値の数: {plots.isnull().sum().sum()}\n")
    
    # 相関係数を計算
    corr_matrix = plots.corr()
    
    # Seabornのpairplotをカスタマイズ（白黒で描画）
    pg = sns.pairplot(plots, diag_kind="hist", 
                      plot_kws={'color': 'black', 's': 30, 'alpha': 0.6},
                      diag_kws={'color': 'black', 'edgecolor': 'black'})
    
    # 下半分の三角形に相関係数を表示
    pg.map_lower(corr_func)
    
    # プロットを保存
    pg.savefig(output_path)
    
    # 相関係数の行列を表示
    print("相関係数行列:")
    print(corr_matrix)
    print()
    
    # matplotlib のフィギュアをクローズしてメモリを解放
    plt.close()
    
    return output_path

