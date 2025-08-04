import requests
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st
import time # 再試行の間に少し待機するためにインポート

####################################################################################
#
# utils: Generate map
# Auther: Satoshi Matsuno
#
####################################################################################


def generate_geological_map(
    lat_min, lat_max, lon_min, lon_max, margin,
    show_xlabel, xlabel_fontsize,
    show_ylabel, ylabel_fontsize,
    label_fontweight,
    show_xticks, xticks_fontsize,
    show_yticks, yticks_fontsize,
    show_grid, override_z = None,
):
    """
    ユーザー入力に基づいて地質図を生成し、matplotlibのfigureオブジェクトと
    PNG形式のダウンロード用データを返す関数
    400エラーの場合はズームレベルを下げて再試行する
    """

    # 選択範囲の広さ（緯度経度の差の大きい方）を計算
    lat_span = abs(lat_max - lat_min)
    lon_span = abs(lon_max - lon_min)
    span = max(lat_span, lon_span)

    # 範囲の広さに応じてズームレベル(z)を動的に決定
    if span > 5.0:
        z = 8
    elif span > 2.5:
        z = 9
    elif span > 1.2:
        z = 10
    elif span > 0.6:
        z = 11
    elif span > 0.3:
        z = 12
    elif span > 0.15:
        z = 13
    elif span > 0.07:
        z = 14
    else:
        z = 15

    # 実際にAPIに渡すズームレベルを final_z として決定する
    if override_z is not None:
        final_z = override_z
    else:
        final_z = z

    # --- ▼▼▼ ここからAPIリクエスト部分を全面的に修正 ▼▼▼ ---

    MIN_ZOOM = 5  # 無限ループを防ぐための最小ズームレベル

    while final_z >= MIN_ZOOM:
        url = "https://gbank.gsj.jp/seamless/v2/api/1.0/map.png"
        bbox = f"{lat_min - margin},{lon_min - margin},{lat_max + margin},{lon_max + margin}"
        params = {'box': bbox, 'z': final_z}

        try:
            # APIにリクエストを送信
            response = requests.get(url, params=params)
            response.raise_for_status()  # 4xx, 5xxエラーの場合に例外を発生させる

            # 成功した場合: 画像を処理してループを抜ける
            image = Image.open(BytesIO(response.content))
            break  # ループを正常に終了

        except requests.exceptions.HTTPError as e:
            # HTTPエラーを捕捉
            if e.response.status_code == 400:
                # 400エラーの場合、ズームレベルを下げて再試行
                st.warning(f"⚠️ ズームレベル {final_z} では画像が大きすぎます。ズームレベルを下げて再試行します...")
                final_z -= 1
                time.sleep(0.5)  # APIサーバーへの負荷を考慮して少し待つ
                continue # ループの先頭に戻って再試行
            else:
                # その他のHTTPエラーの場合
                st.error(f"❌ 地図画像の取得に失敗しました (HTTPエラー): {e}")
                return None, None, None
        except requests.exceptions.RequestException as e:
            # タイムアウトや接続エラーなど、その他のリクエスト関連エラー
            st.error(f"❌ 地図画像の取得に失敗しました (リクエストエラー): {e}")
            return None, None, None
    
    # ループが正常に終了しなかった場合（ズームレベルが下限に達した）
    if final_z < MIN_ZOOM:
        st.error("❌ ズームレベルを調整しても地図を取得できませんでした。指定範囲が広すぎる可能性があります。")
        return None, None, None
    
    # --- ▲▲▲ APIリクエスト部分の修正はここまで ▲▲▲ ---


    # --- グラフの最終調整 ---
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 10))
    img_extent = [
        lon_min - margin, lon_max + margin,
        lat_min - margin, lat_max + margin
    ]
    ax1.imshow(image, extent=img_extent, alpha=0.8, zorder=1)
    ax1.set_rasterized(True)
    
    # (以降の描画コードは変更なし)
    center_lat = np.mean([lat_min, lat_max])
    aspect_ratio = 1 / np.abs(np.cos(np.radians(center_lat)))
    ax1.set_aspect(aspect_ratio)
    
    if show_xlabel:
        ax1.set_xlabel('Longitude', fontsize=xlabel_fontsize, fontweight=label_fontweight)
    if show_ylabel:
        ax1.set_ylabel('Latitude', fontsize=ylabel_fontsize, fontweight=label_fontweight)

    ax1.tick_params(axis='x', labelsize=xticks_fontsize, labelbottom=show_xticks)
    ax1.tick_params(axis='y', labelsize=yticks_fontsize, labelleft=show_yticks)

    if show_grid:
        ax1.grid(True, color="white", linestyle='--', linewidth=0.7, zorder=2)

    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.3f}'))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.3f}'))

    credit_text = "Source: Seamless Digital Geological Map of Japan V2, GSJ, AIST"
    fig.text(0.99, 0.01, credit_text, ha='right', va='bottom', fontsize=7, color='black')

    plt.tight_layout()

    # --- ダウンロード用データの生成 ---
    png_buf = BytesIO()
    plt.savefig(png_buf, format="png", dpi=300)
    png_buf.seek(0)

    # 実際に使用したズームレベル final_z を返す
    return fig, png_buf, final_z