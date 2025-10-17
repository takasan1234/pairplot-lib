"""
CLIメインロジック - ユーザーインターフェースとプロッター統合
"""
import sys
from typing import Optional

from .config import DATA_DIR, OUTPUT_DIR
from .core import (
    list_csv_files,
    select_csv_file,
    load_csv_robust,
    get_numeric_columns,
    select_columns_interactive
)
from .core.file_utils import ensure_output_dir, generate_output_path, get_base_name
from .plotters import (
    create_basic_pairplot,
    create_colored_pairplot,
    create_scatter_boxplot
)


def display_menu() -> int:
    """
    メインメニューを表示してユーザーの選択を取得
    
    Returns:
        選択されたメニュー番号（1-3）
    """
    print("\n" + "=" * 60)
    print("WAO Tech Pairplot - データ可視化ツール")
    print("=" * 60)
    print("\n実行するプロットタイプを選択してください:\n")
    print("1. 基本ペアプロット（相関係数表示）")
    print("   - 数値列を使用してペアプロットを作成")
    print("   - 下三角部分に相関係数を表示")
    print()
    print("2. 色分けペアプロット（z列による分類）")
    print("   - z列の値によってデータを色分け")
    print("   - 注意: データに'z'列が必要です")
    print()
    print("3. 散布図（最もシンプル）")
    print("   - 2変数の散布図を作成")
    print("   - オプションで箱ひげ図も追加可能")
    print("   - z列があれば色分けも可能")
    print()
    print("=" * 60)
    
    while True:
        try:
            choice = int(input("\n選択してください (1-3): "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("1から3の範囲で入力してください。")
        except ValueError:
            print("数字を入力してください。")
        except KeyboardInterrupt:
            print("\n\n処理を中断しました。")
            sys.exit(0)


def run_basic_pairplot(data_dir: str = DATA_DIR, output_dir: str = OUTPUT_DIR) -> None:
    """
    基本ペアプロット（相関係数表示）の実行
    """
    print("\n【基本ペアプロット】")
    
    # 出力ディレクトリを確保
    ensure_output_dir(output_dir)
    
    # CSVファイルの一覧を取得
    csv_files = list_csv_files(data_dir)
    if not csv_files:
        print(f"エラー: {data_dir}フォルダにCSVファイルが見つかりません。")
        sys.exit(1)
    
    # ファイル選択
    selected_file = select_csv_file(csv_files)
    
    # データ読み込み
    df = load_csv_robust(selected_file)
    
    # 数値列の取得
    numeric_cols = get_numeric_columns(df)
    
    # 出力パスの生成
    base_name = get_base_name(selected_file)
    output_path = generate_output_path(output_dir, base_name, "pairplot")
    
    # プロット作成
    result_path = create_basic_pairplot(df, numeric_cols, output_path)
    
    # 結果表示
    print("=" * 50)
    print(f"✓ 画像ファイルを作成しました: {get_base_name(result_path)}.png")
    print(f"  保存先: {result_path}")
    print("=" * 50)


def run_colored_pairplot(data_dir: str = DATA_DIR, output_dir: str = OUTPUT_DIR) -> None:
    """
    色分けペアプロット（z列による分類）の実行
    """
    print("\n【色分けペアプロット】")
    
    # 出力ディレクトリを確保
    ensure_output_dir(output_dir)
    
    # CSVファイルの一覧を取得
    csv_files = list_csv_files(data_dir)
    if not csv_files:
        print(f"エラー: {data_dir}フォルダにCSVファイルが見つかりません。")
        sys.exit(1)
    
    # ファイル選択
    selected_file = select_csv_file(csv_files)
    
    # データ読み込み
    df = load_csv_robust(selected_file)
    
    # 出力パスの生成
    base_name = get_base_name(selected_file)
    output_path = generate_output_path(output_dir, base_name, "pairplot_colored")
    
    # プロット作成
    try:
        result_path = create_colored_pairplot(df, output_path)
        
        # 結果表示
        print("=" * 50)
        print(f"✓ 画像ファイルを作成しました: {get_base_name(result_path)}_colored.png")
        print(f"  保存先: {result_path}")
        print("=" * 50)
    except ValueError as e:
        print(f"\n{e}")
        print("このプロットタイプには'z'列を含むデータが必要です。")
        sys.exit(1)


def run_scatter_boxplot(data_dir: str = DATA_DIR, output_dir: str = OUTPUT_DIR) -> None:
    """
    散布図の実行（箱ひげ図はオプション）
    """
    print("\n【散布図】")
    
    # 出力ディレクトリを確保
    ensure_output_dir(output_dir)
    
    # CSVファイルの一覧を取得
    csv_files = list_csv_files(data_dir)
    if not csv_files:
        print(f"エラー: {data_dir}フォルダにCSVファイルが見つかりません。")
        sys.exit(1)
    
    # ファイル選択
    selected_file = select_csv_file(csv_files)
    
    # データ読み込み
    df = load_csv_robust(selected_file)
    
    # z列が含まれているか確認
    has_z_column = 'z' in df.columns
    
    # プロットに使用する列を選択（z列は除く）
    if has_z_column:
        plot_cols = get_numeric_columns(df, exclude_cols=['z'])
    else:
        plot_cols = get_numeric_columns(df)
    
    print(f"利用可能な数値列: {plot_cols}\n")
    
    if len(plot_cols) < 2:
        print("エラー: 少なくとも2つの数値列が必要です。")
        sys.exit(1)
    
    # X軸の変数を選択
    x_var = select_columns_interactive(plot_cols, "X軸に使用する変数を選択してください:")
    
    # Y軸の変数を選択
    y_var = select_columns_interactive(plot_cols, "\nY軸に使用する変数を選択してください:")
    
    # 箱ひげ図を追加するか確認
    print("\n箱ひげ図を追加しますか？")
    print("1. はい（散布図 + 箱ひげ図）")
    print("2. いいえ（散布図のみ）")
    
    while True:
        try:
            boxplot_choice = int(input("選択 (1-2): "))
            if boxplot_choice in [1, 2]:
                with_boxplot = (boxplot_choice == 1)
                break
            else:
                print("1か2を入力してください。")
        except ValueError:
            print("数字を入力してください。")
        except KeyboardInterrupt:
            print("\n\n処理を中断しました。")
            sys.exit(0)
    
    # 出力パスの生成
    base_name = get_base_name(selected_file)
    if with_boxplot:
        if has_z_column:
            suffix = f"{x_var}_vs_{y_var}_with_boxplot_colored"
        else:
            suffix = f"{x_var}_vs_{y_var}_with_boxplot"
    else:
        if has_z_column:
            suffix = f"{x_var}_vs_{y_var}_colored"
        else:
            suffix = f"{x_var}_vs_{y_var}"
    output_path = generate_output_path(output_dir, base_name, suffix)
    
    # プロット作成
    result_path = create_scatter_boxplot(df, x_var, y_var, output_path, has_z_column, with_boxplot)
    
    # 結果表示
    print("\n" + "=" * 50)
    print(f"✓ 画像ファイルを作成しました: {get_base_name(result_path)}.png")
    print(f"  保存先: {result_path}")
    print("=" * 50)


def main(data_dir: Optional[str] = None, output_dir: Optional[str] = None) -> None:
    """
    メインエントリーポイント
    
    Args:
        data_dir: データディレクトリ（指定がない場合はデフォルト使用）
        output_dir: 出力ディレクトリ（指定がない場合はデフォルト使用）
    """
    # デフォルト値の設定
    if data_dir is None:
        data_dir = DATA_DIR
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    try:
        # メニュー表示と選択
        choice = display_menu()
        
        # 選択に応じて処理を実行
        if choice == 1:
            run_basic_pairplot(data_dir, output_dir)
        elif choice == 2:
            run_colored_pairplot(data_dir, output_dir)
        elif choice == 3:
            run_scatter_boxplot(data_dir, output_dir)
        
    except KeyboardInterrupt:
        print("\n\n処理を中断しました。")
        sys.exit(0)
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

