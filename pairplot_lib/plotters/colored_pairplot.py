"""
色分け識別ありペアプロット
pairplot4.pyの機能を移植
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from .utils import corr_func


def create_colored_pairplot(df: pd.DataFrame, output_path: str, annotation_type: str = "none") -> str:
    """
    色分け識別ありペアプロットを作成（z列による色分け）
    
    Args:
        df: 入力DataFrame（z列を含む必要がある）
        output_path: 出力ファイルパス
        annotation_type: 表示タイプ（"correlation": 相関係数、"regression": 回帰直線、"none": なし）
        
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
    
    # 数値列のみを取得（z列を除く）
    numeric_cols = [col for col in df.columns if col != 'z' and pd.api.types.is_numeric_dtype(df[col])]
    
    # ペアプロットの作成（白黒）
    pg = sns.pairplot(df, hue='z', markers=marker_list, diag_kind="hist",
                      palette=palette, 
                      plot_kws={'edgecolor': 'black', 's': 50, 'linewidth': 1.5, 'alpha': 0.7},
                      diag_kws={'edgecolor': 'black'})
    
    # 凡例を削除
    pg._legend.remove()

    # 表示タイプに応じて下半分の三角形に情報を追加
    if annotation_type == "correlation":
        # 数値列のみで相関係数を計算
        numeric_data = df[numeric_cols]
        corr_matrix = numeric_data.corr()
        
        # 下三角部分の各サブプロットに相関係数を表示
        for i in range(len(numeric_cols)):
            for j in range(i):
                ax = pg.axes[i, j]
                corr_value = corr_matrix.iloc[i, j]
                ax.annotate(f"r = {corr_value:.3f}",
                           xy=(.2, .5),
                           xycoords=ax.transAxes,
                           size=16)
        print("表示オプション: 相関係数を表示")
    
    elif annotation_type == "regression":
        # 下三角部分の各サブプロットに回帰直線を表示
        numeric_data = df[numeric_cols]
        for i in range(len(numeric_cols)):
            for j in range(i):
                ax = pg.axes[i, j]
                
                # プロット内のデータ点を取得して回帰直線を計算
                x_data = numeric_data.iloc[:, j].dropna()
                y_data = numeric_data.iloc[:, i].dropna()
                
                # NaNを除いたデータで回帰を計算
                mask = ~(np.isnan(x_data.values) | np.isnan(y_data.values))
                x_clean = x_data.values[mask]
                y_clean = y_data.values[mask]
                
                if len(x_clean) >= 2:
                    try:
                        slope, intercept, _, _, _ = stats.linregress(x_clean, y_clean)
                        x_line = np.array([x_clean.min(), x_clean.max()])
                        y_line = slope * x_line + intercept
                        ax.plot(x_line, y_line, 'k-', linewidth=2, alpha=0.8)
                    except (ValueError, RuntimeError):
                        pass
        print("表示オプション: 回帰直線を表示")
    
    else:
        print("表示オプション: なし")
    
    # 画像にして保存
    pg.savefig(output_path)
    
    # matplotlib のフィギュアをクローズしてメモリを解放
    plt.close()
    
    return output_path

