"""
散布図と箱ひげ図の組み合わせプロット
scatter_with_boxplot.pyの機能を移植
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from typing import Tuple


def create_scatter_boxplot(
    df: pd.DataFrame,
    x_var: str,
    y_var: str,
    output_path: str,
    has_z_column: bool = False,
    with_boxplot: bool = True
) -> str:
    """
    散布図を作成（オプションで箱ひげ図も追加可能）
    
    Args:
        df: 入力DataFrame
        x_var: X軸の変数名
        y_var: Y軸の変数名
        output_path: 出力ファイルパス
        has_z_column: z列が存在する場合はTrue（色分けする）
        with_boxplot: Trueの場合は箱ひげ図も表示
        
    Returns:
        保存したファイルパス
    """
    if with_boxplot:
        print(f"\n散布図と箱ひげ図を作成中: X={x_var}, Y={y_var}")
    else:
        print(f"\n散布図を作成中: X={x_var}, Y={y_var}")
    
    # レイアウトの作成（箱ひげ図の有無で変更）
    if with_boxplot:
        # GridSpecを使用してレイアウトを作成
        fig = plt.figure(figsize=(12, 10))
        gs = GridSpec(3, 3, figure=fig, 
                      width_ratios=[1, 4, 0.5], 
                      height_ratios=[1, 4, 0.5],
                      hspace=0.05, wspace=0.05)
        
        # メインの散布図
        ax_scatter = fig.add_subplot(gs[1, 1])
        
        # 上部の箱ひげ図（X軸方向）
        ax_box_x = fig.add_subplot(gs[0, 1], sharex=ax_scatter)
        
        # 右側の箱ひげ図（Y軸方向）
        ax_box_y = fig.add_subplot(gs[1, 2], sharey=ax_scatter)
    else:
        # 散布図のみの場合はシンプルなレイアウト
        fig, ax_scatter = plt.subplots(figsize=(10, 8))
    
    # z列がある場合は色分けして描画（散布図のみ）
    if has_z_column and 'z' in df.columns:
        unique_z = sorted(df['z'].unique())
        print(f"z列のユニークな値: {unique_z}")
        
        # 白黒の色設定（黒丸と白抜き丸）
        colors = ['black', 'white']
        edgecolors = ['black', 'black']
        markers = ['o', 'o']
        
        # 散布図の描画（凡例なし）
        for idx, z_val in enumerate(unique_z):
            df_subset = df[df['z'] == z_val]
            color_idx = idx % 2
            
            ax_scatter.scatter(df_subset[x_var], df_subset[y_var],
                              c=colors[color_idx],
                              edgecolors=edgecolors[color_idx],
                              marker=markers[color_idx],
                              s=100,
                              linewidth=1.5,
                              alpha=0.7)
    else:
        # z列がない場合は通常の散布図（黒丸）
        ax_scatter.scatter(df[x_var], df[y_var], c='black', alpha=0.7, s=100)
    
    # 散布図の設定
    ax_scatter.set_xlabel(x_var, fontsize=14)
    ax_scatter.set_ylabel(y_var, fontsize=14)
    ax_scatter.grid(True, alpha=0.3)
    
    # 箱ひげ図を描画する場合のみ
    if with_boxplot:
        # 箱ひげ図の描画（z値に関係なく全データを1つの箱ひげ図に、白黒）
        x_data = df[x_var].dropna()
        y_data = df[y_var].dropna()
        
        # X軸方向の箱ひげ図（横向き、白黒）
        bp_x = ax_box_x.boxplot([x_data], vert=False, positions=[0],
                                 widths=0.5, patch_artist=True, showcaps=True,
                                 boxprops=dict(facecolor='white', edgecolor='black', linewidth=1.5),
                                 medianprops=dict(color='black', linewidth=2),
                                 whiskerprops=dict(color='black', linewidth=1.5),
                                 capprops=dict(color='black', linewidth=1.5))
        
        # Y軸方向の箱ひげ図（縦向き、白黒）
        bp_y = ax_box_y.boxplot([y_data], vert=True, positions=[0],
                                 widths=0.5, patch_artist=True, showcaps=True,
                                 boxprops=dict(facecolor='white', edgecolor='black', linewidth=1.5),
                                 medianprops=dict(color='black', linewidth=2),
                                 whiskerprops=dict(color='black', linewidth=1.5),
                                 capprops=dict(color='black', linewidth=1.5))
        
        # 箱ひげ図の軸設定と枠線削除
        # X軸方向の箱ひげ図
        ax_box_x.set_yticks([])
        ax_box_x.set_ylim(-0.8, 0.8)  # 箱ひげ図の表示範囲を制限
        ax_box_x.tick_params(labelbottom=False, bottom=False, left=False)
        ax_box_x.spines['top'].set_visible(False)
        ax_box_x.spines['right'].set_visible(False)
        ax_box_x.spines['bottom'].set_visible(False)
        ax_box_x.spines['left'].set_visible(False)
        
        # Y軸方向の箱ひげ図
        ax_box_y.set_xticks([])
        ax_box_y.set_xlim(-0.8, 0.8)  # 箱ひげ図の表示範囲を制限
        ax_box_y.tick_params(labelleft=False, left=False, bottom=False)
        ax_box_y.spines['top'].set_visible(False)
        ax_box_y.spines['right'].set_visible(False)
        ax_box_y.spines['bottom'].set_visible(False)
        ax_box_y.spines['left'].set_visible(False)
        
        # 全体のタイトル
        fig.suptitle(f'{x_var} vs {y_var} (散布図 + 箱ひげ図)', fontsize=16, y=0.98)
    else:
        # 散布図のみの場合のタイトル
        fig.suptitle(f'{x_var} vs {y_var}', fontsize=16)
    
    # 画像を保存
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    # matplotlib のフィギュアをクローズしてメモリを解放
    plt.close()
    
    return output_path

