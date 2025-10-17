# Pairplot

CSVデータから白黒のペアプロット・散布図を自動生成するツール

## インストール

```bash
pip install "git+https://github.com/takasan1234/pairplot-lib.git@v1.0.1"
```

> バージョンを指定しない場合は最新版がインストールされます：
> ```bash
> pip install "git+https://github.com/takasan1234/pairplot-lib.git"
> ```

## 使い方

### 1. 作業ディレクトリを準備

任意の場所に作業ディレクトリを作成し、そこで作業します：

```bash
mkdir my_analysis
cd my_analysis
mkdir data
mkdir output
```

### 2. データを配置

CSVファイルを`data/`フォルダに入れます：

```bash
cp your_data.csv data/
```

### 3. コマンド実行

```bash
pairplot
```

または

```bash
python -m pairplot_lib
```

> **注意**: コマンドは作業ディレクトリ内で実行してください。
> カレントディレクトリの`data/`と`output/`が使用されます。

## 3つの機能

### 1. 基本ペアプロット
- 全ての数値列のペアプロット
- 相関係数を自動表示
- 使い道：データの全体像を把握

### 2. 色分けペアプロット
- z列による分類（黒丸・白抜き丸）
- データに`z`列が必要
- 使い道：グループ間の比較

### 3. 散布図
- 2変数を選んで散布図作成
- 箱ひげ図の追加も選択可能
- z列があれば色分けも可能
- 使い道：特定の変数の関係を詳しく見る

## データフォーマット

- タブ区切り、カンマ区切り、どちらでもOK
- 数値列が2列以上あれば使える
- 1行目に列名が必要

## 出力

`output/`フォルダに画像が保存されます：

- `{ファイル名}_pairplot.png` - 基本ペアプロット
- `{ファイル名}_pairplot_colored.png` - 色分けペアプロット
- `{ファイル名}_a_vs_b.png` - 散布図
- `{ファイル名}_a_vs_b_with_boxplot.png` - 散布図+箱ひげ図

## トラブルシューティング

### コマンドが見つからない
```bash
# 再インストール
pip install --force-reinstall "git+https://github.com/takasan1234/pairplot-lib.git@v1.0.1"
```

### データが見つからない
- `data/`フォルダにCSVがあるか確認
- CSVの1行目に列名があるか確認

---

**作者**: Takayuki Tsuji  
**バージョン**: 1.0.1
