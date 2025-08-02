# 🗺️ Geological Map Maker (地質図作成アプリ)

[![Python](https://img.shields.io/badge/Python-%3E%3D3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47%2B-red.svg)](https://streamlit.io)
[![Poetry](https://img.shields.io/badge/Poetry-2.0%2B-purple.svg)](https://python-poetry.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

産総研（AIST）の地質図APIを利用して、指定した緯度・経度の範囲の地質図をインタラクティブに生成し、表示をカスタマイズできるStreamlitアプリケーションです。

This is a Streamlit application that allows you to interactively generate and customize geological maps for a specified latitude and longitude range, using the AIST (GSJ) "Seamless Geological Map v2" API.

---

## ✨ 主な機能

-   **範囲指定**: 緯度と経度を入力して、表示したい地質図の範囲を自由に設定できます。
-   **表示カスタマイズ**: 軸ラベル、目盛り、グリッドの表示/非表示やフォントサイズをGUIで簡単に変更できます。
-   **画像ダウンロード**: 生成した地質図を、高解像度のPNG形式またはベクター形式のPDFでダウンロードできます。

---

## 🛠️ 依存関係 (Dependencies)

このプロジェクトは[Poetry](https://python-poetry.org/)で管理されています。
必要なライブラリとバージョンは`pyproject.toml`で定義されています。

```toml
[tool.poetry.dependencies]
python = ">=3.11"
streamlit = ">=1.47.1,<2.0.0"
matplotlib = ">=3.10.5,<4.0.0"
requests = ">=2.32.4,<3.0.0"
pillow = ">=11.3.0,<12.0.0"
numpy = ">=2.3.2,<3.0.0"
````

-----

## 🚀 インストールと実行方法

### 1\. 前提条件

* [Python](https://www.python.org/downloads/) (3.11以上)

* [Poetry](https://python-poetry.org/docs/#installation) (2.0以上)


### 2\. セットアップ

リポジトリをクローンし、ディレクトリに移動します。

```bash
git clone <repository-url>
cd Geological_map_maker
```

Poetryを使用して、必要なライブラリをインストールします。

```bash
poetry install
```

### 3\. アプリケーションの実行

以下のコマンドでStreamlitサーバーを起動します。

```bash
poetry run streamlit run app.py
```

*(注意: `app.py`は、実際のスクリプトファイル名に置き換えてください)*

ブラウザで `http://localhost:8501` にアクセスすると、アプリケーションが表示されます。

-----

## ⚙️ 使い方

1.  画面左のサイドバーで、地質図を表示したい範囲の**緯度**と**経度**（最大・最小）を入力します。
2.  必要に応じて、地図の余白や、ラベル・グリッドの表示設定を調整します。
3.  メイン画面に生成された地質図が表示されます。
4.  「画像をダウンロード (.png)」または「PDFをダウンロード (.pdf)」ボタンをクリックすると、表示されている地図をファイルとして保存できます。

-----

## 🙏 謝辞・データソース

このアプリケーションは、[産業技術総合研究所 地質調査総合センター (GSJ)](https://www.gsj.jp/) の「**シームレス地質図v2**」Web APIサービスを利用して作成されました。
データの利用にあたっては、GSJの定める[利用規約](https://www.google.com/search?q=https://gbank.gsj.jp/seamless/v2/policy.html)を遵守してください。

-----

## 👤 作者 (Author)

  - [Satoshi Matsuno](https://researchmap.jp/satoshi_matsuno)

-----

## 📜 ライセンス (License)

このプロジェクトはMITライセンスの下で公開されています。