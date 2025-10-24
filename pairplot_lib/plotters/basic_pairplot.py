"""
基本的なペアプロット（相関係数表示付き）
pairplot2.pyの機能を移植
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .utils import corr_func, regress_func


def create_basic_pairplot(df: pd.DataFrame, numeric_cols: list, output_path: str, annotation_type: str = "none") -> str:
    """
    基本的なペアプロット（相関係数表示付き）を作成
    
    Args:
        df: 入力DataFrame
        numeric_cols: プロットする数値列のリスト
        output_path: 出力ファイルパス
        annotation_type: 表示タイプ（"correlation": 相関係数、"regression": 回帰直線、"none": なし）
        
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
    
    # 表示タイプに応じて下半分の三角形に情報を追加
    if annotation_type == "correlation":
        pg.map_lower(corr_func)
        print("表示オプション: 相関係数を表示")
    elif annotation_type == "regression":
        pg.map_lower(regress_func)
        print("表示オプション: 回帰直線を表示")
    else:
        print("表示オプション: なし")
    
    # プロットを保存
    pg.savefig(output_path)
    
    # 相関係数の行列を表示（相関係数表示の場合のみ）
    if annotation_type == "correlation":
        print("\n相関係数行列:")
        print(corr_matrix)
        print()
    
    # matplotlib のフィギュアをクローズしてメモリを解放
    plt.close()
    
    return output_path

