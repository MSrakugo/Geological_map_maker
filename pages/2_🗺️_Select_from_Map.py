import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import numpy as np
from utils import generate_geological_map # 共通関数をインポート

####################################################################################
#
# Main: Page 2 for selecting a region on the map 
# Auther: Satoshi Matsuno
#
####################################################################################

st.set_page_config(layout="wide")
st.title("🗺️ 地質図作成アプリ")
st.markdown("### 2. 地図上で範囲を選択して作成")

# --- サイドバーの設定 ---
with st.sidebar:

    manual_zoom = st.checkbox("ズームレベルを手動で設定する")
    override_z = None
    if manual_zoom:
        override_z = st.slider("手動ズームレベル", min_value=5, max_value=18, value=12)

    st.header("🎨 ラベルとグリッドの設定")
    label_fontweight = st.selectbox('ラベルのフォントの太さ', ('normal', 'bold'), index=0, key="fontweight_2")
    show_xlabel = st.toggle('X軸ラベルを表示', value=True, key="show_xlabel_2")
    xlabel_fontsize = st.slider('X軸ラベルのフォントサイズ', 6, 20, 12, disabled=not show_xlabel, key="xlabel_fs_2")
    show_ylabel = st.toggle('Y軸ラベルを表示', value=True, key="show_ylabel_2")
    ylabel_fontsize = st.slider('Y軸ラベルのフォントサイズ', 6, 20, 12, disabled=not show_ylabel, key="ylabel_fs_2")
    show_xticks = st.toggle('X軸目盛りを表示', value=True, key="show_xticks_2")
    xticks_fontsize = st.slider('X軸目盛りのフォントサイズ', 6, 20, 10, disabled=not show_xticks, key="xticks_fs_2")
    show_yticks = st.toggle('Y軸目盛りを表示', value=True, key="show_yticks_2")
    yticks_fontsize = st.slider('Y軸目盛りのフォントサイズ', 6, 20, 10, disabled=not show_yticks, key="yticks_fs_2")
    show_grid = st.toggle('グリッドを表示', value=True, key="show_grid_2")
    margin = st.number_input('地図範囲の余白', value=0.01, format="%.4f", key="margin_2")

# --- メイン画面 ---
st.info("💡 **使い方**: 左上の四角形アイコンをクリックし、地図上でドラッグして範囲を選択してください。")

# 地図の初期設定（日本の中心あたり）
m = folium.Map(location=[36.2048, 138.2529], zoom_start=5)

# 地図に描画ツールを追加
Draw(
    export=True,
    filename='data.geojson',
    position='topleft',
    draw_options={'rectangle': {'shapeOptions': {'color': "#ffa200"}}}, # 四角形のみ許可
    edit_options={'edit': False}
).add_to(m)

# Streamlitで地図を表示
map_data = st_folium(m, width=800, height=600)

# 描画されたデータがあれば地質図を生成
if map_data.get("last_active_drawing"):
    # 最後に描画された四角形の座標を取得
    coords = map_data["last_active_drawing"]["geometry"]["coordinates"][0]
    
    # 緯度と経度のリストに分割
    lats = [c[1] for c in coords]
    lons = [c[0] for c in coords]

    # 最大・最小の緯度経度を計算
    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)
    
    st.write("---")
    st.subheader("選択された範囲の座標")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"最小緯度: `{lat_min:.4f}`")
        st.write(f"最大緯度: `{lat_max:.4f}`")
    with col2:
        st.write(f"最小経度: `{lon_min:.4f}`")
        st.write(f"最大経度: `{lon_max:.4f}`")

    st.subheader("生成された地質図")
    
    with st.spinner('地質図を生成中です...'):
        # 戻り値のズームレベルの変数名を final_z に変更（分かりやすさのため）
        fig, png_data, final_z = generate_geological_map(
            lat_min, lat_max, lon_min, lon_max, margin,
            show_xlabel, xlabel_fontsize,
            show_ylabel, ylabel_fontsize,
            label_fontweight,
            show_xticks, xticks_fontsize,
            show_yticks, yticks_fontsize,
            show_grid, override_z
        )

    if fig and png_data:
        # 実際に使用されたズームレベルをユーザーに通知
        st.info(f"ℹ️ ズームレベル {final_z} で地図を取得しました。")

    if fig and png_data:
        st.pyplot(fig)
        st.caption("地図データ出典：産総研地質調査総合センター「シームレス地質図v2」")

        st.download_button(
            label="📥 画像をダウンロード (.png)",
            data=png_data,
            file_name=f"geological_map_{lat_min:.2f}_{lon_min:.2f}.png",
            mime="image/png"
        )
else:
    st.write("---")
    st.warning("地質図を表示するには、地図上で範囲を選択してください。")