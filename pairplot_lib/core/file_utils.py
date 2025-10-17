"""
ファイル操作のためのユーティリティ関数
"""
import os
from typing import Optional


def ensure_output_dir(output_dir: str) -> None:
    """
    出力ディレクトリが存在しない場合は作成する
    
    Args:
        output_dir: 出力ディレクトリのパス
    """
    os.makedirs(output_dir, exist_ok=True)


def generate_output_path(
    output_dir: str,
    base_name: str,
    suffix: str,
    extension: str = "png"
) -> str:
    """
    出力ファイルのパスを生成
    
    Args:
        output_dir: 出力ディレクトリのパス
        base_name: ベースファイル名（拡張子なし）
        suffix: ファイル名に追加するサフィックス
        extension: ファイル拡張子（デフォルト: "png"）
        
    Returns:
        完全な出力ファイルパス
    """
    output_file_name = f"{base_name}_{suffix}.{extension}"
    return os.path.join(output_dir, output_file_name)


def get_base_name(file_path: str) -> str:
    """
    ファイルパスからベース名（拡張子なし）を取得
    
    Args:
        file_path: ファイルパス
        
    Returns:
        ベースファイル名
    """
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    return base_name

