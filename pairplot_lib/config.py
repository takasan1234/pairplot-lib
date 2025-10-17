"""
設定ファイル - データディレクトリと出力ディレクトリの管理
"""
import os

# カレントディレクトリ（コマンドを実行する場所）を基準にする
# これにより、ユーザーはどこからでもコマンドを実行でき、
# そのディレクトリのdata/とoutput/を使用できる
CURRENT_DIR = os.getcwd()

# データフォルダと出力フォルダのデフォルトパス
DATA_DIR = os.path.join(CURRENT_DIR, 'data')
OUTPUT_DIR = os.path.join(CURRENT_DIR, 'output')

