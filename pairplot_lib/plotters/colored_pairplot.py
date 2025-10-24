"""
色分け識別ありペアプロット
pairplot4.pyの機能を移植
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .utils import corr_func


def create_colored_pairplot(df: pd.DataFrame, output_path: str, show_correlation: bool = False) -> str:
    """
    色分け識別ありペアプロットを作成（z列による色分け）
    
    Args:
        df: 入力DataFrame（z列を含む必要がある）
        output_path: 出力ファイルパス
        show_correlation: 相関係数を表示するかどうか
        
    Returns:
        保存したファイルパス
    """
    # z列が存在するかチェック
    if 'z' not in df.columns:
        raise ValueError("エラー: 'z' 列が見つかりません。色分けには 'z' 列が必要です。")
    
    # 列情報を表示
    print(f"利用可能な列: {df.columns.tolist()}\n")
    
    # z列のユニークな値を取得
    unique_z = sorted(df['z'].unique())
    print(f"z列のユニークな値: {unique_z}\n")
    
    # 白黒のパレット設定（黒と白のみ）
    # 黒丸（塗りつぶし）と白抜き丸で区別
    palette = {unique_z[0]: 'black', unique_z[1]: 'white' if len(unique_z) > 1 else 'black'}
    
    # マーカーは全て丸（'o'）に統一
    marker_list = ['o'] * len(unique_z)
    
    # ペアプロットの作成（白黒）
    pg = sns.pairplot(df, hue='z', markers=marker_list, diag_kind="hist",
                      palette=palette, 
                      plot_kws={'edgecolor': 'black', 's': 50, 'linewidth': 1.5, 'alpha': 0.7},
                      diag_kws={'edgecolor': 'black'})
    
    # 相関係数を表示する場合のみ、下半分の三角形に相関係数を表示
    if show_correlation:
        pg.map_lower(corr_func)
    
    # 凡例を削除
    pg._legend.remove()
    
    # 画像にして保存
    pg.savefig(output_path)
    
    # matplotlib のフィギュアをクローズしてメモリを解放
    plt.close()
    
    return output_path

