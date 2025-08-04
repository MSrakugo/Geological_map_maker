import streamlit as st
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.ticker as ticker
import utils

####################################################################################
#
# Main: Page 1 for manual input
# Auther: Satoshi Matsuno
#
####################################################################################

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

    manual_zoom = st.checkbox("ズームレベルを手動で設定する")
    override_z = None
    if manual_zoom:
        override_z = st.slider("手動ズームレベル", min_value=5, max_value=18, value=12)

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

fig, png_data, _ = utils.generate_geological_map(
    lat_min, lat_max, lon_min, lon_max, margin,
    show_xlabel, xlabel_fontsize,
    show_ylabel, ylabel_fontsize,
    label_fontweight,
    show_xticks, xticks_fontsize,
    show_yticks, yticks_fontsize,
    show_grid
)

if fig and png_data:
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