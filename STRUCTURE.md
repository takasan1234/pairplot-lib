# プロジェクト構造

## 📁 最終的なディレクトリ構造

```
pairplot-lib/
├── 📂 data/                          # サンプルデータ（GitHub追跡）
│   ├── electric_data_chihou.csv
│   ├── electronic_data_rate.csv
│   └── sample_data.csv               # ★ z列の使い方を示すサンプル
│
├── 📂 output/                        # 生成された画像（GitHub除外）
│   ├── electronic_data_rate_a_vs_b_with_boxplot.png
│   ├── electronic_data_rate_a_vs_b_with_boxplot_colored.png
│   ├── electronic_data_rate_pairplot.png
│   └── electronic_data_rate_pairplot_colored.png
│
├── 📂 pairplot_lib/              # メインパッケージ
│   ├── 📂 core/                      # コアモジュール
│   │   ├── __init__.py
│   │   ├── data_loader.py           # CSV読み込み・選択
│   │   └── file_utils.py            # ファイル操作
│   │
│   ├── 📂 plotters/                  # プロッター
│   │   ├── __init__.py
│   │   ├── basic_pairplot.py        # 相関係数付きペアプロット
│   │   ├── colored_pairplot.py      # 色分けペアプロット
│   │   └── scatter_boxplot.py       # 散布図+箱ひげ図
│   │
│   ├── __init__.py                   # パッケージ初期化 (v1.0.1)
│   ├── __main__.py                   # python -m エントリーポイント
│   ├── cli.py                        # CLIメインロジック
│   └── config.py                     # 設定（カレントディレクトリ基準）
│
├── 📄 .gitignore                     # Git除外設定
├── 📄 CHANGELOG.md                   # 変更履歴
├── 📄 QUICKSTART.md                  # クイックスタートガイド ★
├── 📄 README.md                      # プロジェクト概要 ★
├── 📄 requirements.txt               # 依存パッケージ
└── 📄 setup.py                       # インストール設定

6 directories, 23 files
```

## 🎯 重要なファイル

### 利用者向けドキュメント
- **QUICKSTART.md** - 使い方（ステップバイステップ）
- **README.md** - プロジェクト概要と機能説明
- **data/sample_data.csv** - サンプルデータ（z列の使い方を示す）

### 開発者向けドキュメント
- **CHANGELOG.md** - バージョン履歴
- **setup.py** - パッケージ設定
- **requirements.txt** - 依存パッケージリスト

## 📝 Git管理

### GitHub追跡対象
✅ 全てのソースコード（`pairplot_lib/`）  
✅ ドキュメント（`*.md`）  
✅ 設定ファイル（`setup.py`, `requirements.txt`, `.gitignore`）  
✅ サンプルデータ（`data/sample_data.csv`のみ）

### GitHub除外対象
❌ `data/*`（サンプル以外のCSV）  
❌ `output/`（生成された画像）  
❌ `__pycache__/`, `*.pyc`（Pythonキャッシュ）  
❌ `.venv/`, `.egg-info/`（開発環境）

## 🚀 インストール後の構造

GitHubからインストールした場合、ユーザーは以下の構造で作業します：

```
my_analysis/                          # ユーザーの作業ディレクトリ
├── data/                             # ユーザーが作成
│   └── your_data.csv                 # ユーザーのデータ
└── output/                           # ユーザーが作成
    └── your_data_pairplot.png        # 生成された画像
```

コマンド`wao-pairplot`は、カレントディレクトリの`data/`と`output/`を使用します。

