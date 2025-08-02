import streamlit as st
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.ticker as ticker

def generate_geological_map(
    lat_min, lat_max, lon_min, lon_max, margin,
    show_xlabel, xlabel_fontsize,
    show_ylabel, ylabel_fontsize,
    label_fontweight,
    show_xticks, xticks_fontsize,
    show_yticks, yticks_fontsize,
    show_grid
):
    """
    ユーザー入力に基づいて地質図を生成し、matplotlibのfigureオブジェクトと
    PNG・PDF形式のダウンロード用データを返す関数
    """
    # プロットの準備
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 10))

    # APIリクエストのURL
    url = "https://gbank.gsj.jp/seamless/v2/api/1.0/map.png"
    bbox = f"{lat_min - margin},{lon_min - margin},{lat_max + margin},{lon_max + margin}"
    params = {'box': bbox, 'z': 13}

    try:
        # APIにリクエストを送信
        response = requests.get(url, params=params)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        img_extent = [
            lon_min - margin, lon_max + margin,
            lat_min - margin, lat_max + margin
        ]
        ax1.imshow(image, extent=img_extent, alpha=0.8, zorder=1)
        
        # [修正] 地図レイヤーをラスタライズし、PDFに画像が正しく埋め込まれるようにする
        ax1.set_rasterized(True)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ 地図画像の取得に失敗しました (HTTPエラー): {e}")
        return None, None, None
    except Image.UnidentifiedImageError:
        st.error("❌ 取得したデータは画像ファイルではありません。APIからエラーが返された可能性があります。")
        st.text(f"サーバーからの応答: {response.text}")
        return None, None, None

    # --- グラフの最終調整 ---
    center_lat = np.mean([lat_min, lat_max])
    aspect_ratio = 1 / np.abs(np.cos(np.radians(center_lat)))
    ax1.set_aspect(aspect_ratio)
    
    # X軸・Y軸ラベルの設定
    if show_xlabel:
        ax1.set_xlabel('Longitude', fontsize=xlabel_fontsize, fontweight=label_fontweight)
    if show_ylabel:
        ax1.set_ylabel('Latitude', fontsize=ylabel_fontsize, fontweight=label_fontweight)

    # X軸・Y軸の目盛りと目盛りラベルの設定
    ax1.tick_params(axis='x', labelsize=xticks_fontsize, labelbottom=show_xticks)
    ax1.tick_params(axis='y', labelsize=yticks_fontsize, labelleft=show_yticks)

    # グリッドの設定
    if show_grid:
        ax1.grid(True, color="white", linestyle='--', linewidth=0.7, zorder=2)

    # 軸の目盛りフォーマットを設定
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.3f}'))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.3f}'))

    # 出典を画像内に追加
    credit_text = "Source: Seamless Digital Geological Map of Japan V2, GSJ, AIST"
    fig.text(0.99, 0.01, credit_text, ha='right', va='bottom', fontsize=7, color='black')

    plt.tight_layout()

    # --- ダウンロード用データの生成 ---
    # PNG形式でメモリ上に保存
    png_buf = BytesIO()
    plt.savefig(png_buf, format="png", dpi=300)
    png_buf.seek(0)

    # PDF形式でメモリ上に保存
    pdf_buf = BytesIO()
    # [修正] PDF保存時にも解像度(dpi)を指定し、画質の劣化を防ぐ
    plt.savefig(pdf_buf, format="pdf", dpi=300)
    pdf_buf.seek(0)

    return fig, png_buf, pdf_buf

# --- Streamlit アプリケーションのUI部分 ---
st.set_page_config(layout="wide")
st.title('🗺️ 地質図作成アプリ')

# サイドバーに設定項目を配置
with st.sidebar:
    st.header("⚙️ 地図の範囲設定")
    col1, col2 = st.columns(2)
    with col1:
        lat_min = st.number_input('最小緯度', value=33.7500, format="%.4f")
        lat_max = st.number_input('最大緯度', value=34.0000, format="%.4f")
        
    with col2:
        lon_min = st.number_input('最小経度', value=133.2500, format="%.4f")
        lon_max = st.number_input('最大経度', value=133.7000, format="%.4f")
    margin = st.number_input('地図範囲の余白', value=0.01, format="%.4f")

    st.header("🎨 ラベルとグリッドの設定")
    label_fontweight = st.selectbox('ラベルのフォントの太さ', ('normal', 'bold'), index=0)

    # X軸ラベル
    show_xlabel = st.toggle('X軸ラベルを表示', value=True)
    xlabel_fontsize = st.slider('X軸ラベルのフォントサイズ', 6, 20, 12, disabled=not show_xlabel)

    # Y軸ラベル
    show_ylabel = st.toggle('Y軸ラベルを表示', value=True)
    ylabel_fontsize = st.slider('Y軸ラベルのフォントサイズ', 6, 20, 12, disabled=not show_ylabel)

    # X軸目盛り
    show_xticks = st.toggle('X軸目盛りを表示', value=True)
    xticks_fontsize = st.slider('X軸目盛りのフォントサイズ', 6, 20, 10, disabled=not show_xticks)

    # Y軸目盛り
    show_yticks = st.toggle('Y軸目盛りを表示', value=True)
    yticks_fontsize = st.slider('Y軸目盛りのフォントサイズ', 6, 20, 10, disabled=not show_yticks)

    # グリッド
    show_grid = st.toggle('グリッドを表示', value=True)

# メイン画面で地図を生成・表示
st.subheader("生成された地質図")

fig, png_data, pdf_data = generate_geological_map(
    lat_min, lat_max, lon_min, lon_max, margin,
    show_xlabel, xlabel_fontsize,
    show_ylabel, ylabel_fontsize,
    label_fontweight,
    show_xticks, xticks_fontsize,
    show_yticks, yticks_fontsize,
    show_grid
)

if fig and png_data and pdf_data:
    # 画面に地図を表示
    st.pyplot(fig)
    # アプリ画面上に出典を明記
    st.caption("地図データ出典：産総研地質調査総合センター「シームレス地質図v2」")

    st.download_button(
        label="📥 画像をダウンロード (.png)",
        data=png_data,
        file_name="geological_map.png",
        mime="image/png"
    )
    st.download_button(
        label="📥 PDFをダウンロード (.pdf)",
        data=pdf_data,
        file_name="geological_map.pdf",
        mime="application/pdf"
    )