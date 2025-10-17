"""
データ読み込みと選択のための共通ロジック
"""
import os
import glob
from typing import List, Tuple, Optional
import pandas as pd
import numpy as np


def list_csv_files(data_dir: str) -> List[str]:
    """
    指定されたディレクトリからCSVファイルの一覧を取得
    
    Args:
        data_dir: データディレクトリのパス
        
    Returns:
        CSVファイルのパスのリスト（ソート済み）
    """
    csv_files = sorted(glob.glob(os.path.join(data_dir, '*.csv')))
    return csv_files


def select_csv_file(csv_files: List[str]) -> str:
    """
    ユーザーにCSVファイルを選択させる
    
    Args:
        csv_files: CSVファイルパスのリスト
        
    Returns:
        選択されたファイルのパス
    """
    if not csv_files:
        raise ValueError("CSVファイルが見つかりません。")
    
    # ファイル一覧を表示
    print("=" * 50)
    print("使用可能なCSVファイル:")
    print("=" * 50)
    for idx, file_path in enumerate(csv_files, 1):
        file_name = os.path.basename(file_path)
        print(f"{idx}. {file_name}")
    print("=" * 50)
    
    # ユーザーに選択させる
    while True:
        try:
            choice = int(input(f"\n使用するファイルの番号を選択してください (1-{len(csv_files)}): "))
            if 1 <= choice <= len(csv_files):
                selected_file = csv_files[choice - 1]
                break
            else:
                print(f"1から{len(csv_files)}の範囲で入力してください。")
        except ValueError:
            print("数字を入力してください。")
    
    file_name = os.path.basename(selected_file)
    print(f"\n選択されたファイル: {file_name}")
    print("処理中...\n")
    
    return selected_file


def load_csv_robust(file_path: str) -> pd.DataFrame:
    """
    様々な区切り文字に対応した堅牢なCSV読み込み
    タブ、カンマ、セミコロン、空白区切りなどを自動判定
    
    Args:
        file_path: CSVファイルのパス
        
    Returns:
        読み込まれたDataFrame
    """
    # 1) 自動検出（タブ/カンマ/セミコロンなど）
    try:
        df_auto = pd.read_csv(file_path, sep=None, engine='python', comment='#')
        df_auto.columns = df_auto.columns.str.strip()
        if len(df_auto.columns) > 1:
            return df_auto
    except Exception:
        pass
    
    # 2) 任意空白（タブ＋空白混在も分割）
    try:
        df_ws = pd.read_csv(file_path, sep=r"\s+", engine='python', comment='#')
        df_ws.columns = df_ws.columns.str.strip()
        if len(df_ws.columns) > 1:
            return df_ws
    except Exception:
        pass
    
    # 3) タブ区切り
    try:
        df_tab = pd.read_csv(file_path, sep='\t', comment='#')
        df_tab.columns = df_tab.columns.str.strip()
        if len(df_tab.columns) > 1:
            return df_tab
    except Exception:
        pass
    
    # 4) カンマ区切り（最終手段）
    df_comma = pd.read_csv(file_path, sep=',', comment='#')
    df_comma.columns = df_comma.columns.str.strip()
    return df_comma


def get_numeric_columns(df: pd.DataFrame, exclude_cols: Optional[List[str]] = None) -> List[str]:
    """
    DataFrameから数値列を取得
    
    Args:
        df: DataFrame
        exclude_cols: 除外する列名のリスト
        
    Returns:
        数値列名のリスト
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if exclude_cols:
        numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    return numeric_cols


def select_columns_interactive(columns: List[str], prompt: str) -> str:
    """
    ユーザーに列を選択させる
    
    Args:
        columns: 選択可能な列名のリスト
        prompt: 表示するプロンプトメッセージ
        
    Returns:
        選択された列名
    """
    print(prompt)
    for idx, col in enumerate(columns, 1):
        print(f"{idx}. {col}")
    
    while True:
        try:
            choice = int(input(f"選択 (1-{len(columns)}): "))
            if 1 <= choice <= len(columns):
                return columns[choice - 1]
            else:
                print(f"1から{len(columns)}の範囲で入力してください。")
        except ValueError:
            print("数字を入力してください。")

