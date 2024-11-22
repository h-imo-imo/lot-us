import streamlit as st
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import requests
from io import StringIO


# スプレッドシートIDを指定
SPREADSHEET_ID = '1f7sbENV3Szl5MFWEK1D-IZyQWGfPHYOHYtg7KW-ettQ'
SHEET_NAME = 'シート1'

colors = [
    "#F8B500",
    "#5383C3",
    "#68BE8D",
    "#BA2636",
    "#E7609E",
    "#A2D7DD",
    "#FAD764",
    "#9D8DE2"
]


@st.cache_resource
def load_data(sheet_id: str, sheet_name: str):
    # 公開スプレッドシートのCSVリンク
    url = (
        f'https://docs.google.com/spreadsheets/d/{sheet_id}'
        + f'/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    )

    # データを取得して表示
    response = requests.get(url)
    response = response.content.decode("utf-8")
    df = pd.read_csv(StringIO(response))
    return df


def write_data(data: pd.DataFrame):
    data.to_csv("data.csv", header=False, index=False)


def plot_scatter(df: pd.DataFrame, tag_column: str):
    # 図と軸を作成
    fig, ax = plt.subplots()
    categorys = df[tag_column].unique()

    # 散布図を描画
    for i, cg in enumerate(categorys):
        select_df = df.loc[df[tag_column] == cg]
        ax.scatter(
            select_df["列"],
            select_df["番号"],
            label=cg,
            color=colors[i],
            marker='s'
        )

    # 凡例をグラフの外に配置
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    # 軸ラベルを削除
    ax.set_xlabel('')
    ax.set_ylabel('')

    # タイトルを削除
    ax.set_title('')

    # 軸の目盛りを非表示にする
    ax.set_xticks([])  # X軸の目盛りを削除
    ax.set_yticks([])  # Y軸の目盛りを削除

    # 軸自体も非表示にする
    ax.spines['top'].set_visible(False)  # 上の軸を非表示
    ax.spines['right'].set_visible(False)  # 右の軸を非表示
    ax.spines['left'].set_visible(False)  # 左の軸を非表示
    ax.spines['bottom'].set_visible(False)  # 下の軸を非表示

    # グラフの表示
    st.pyplot(fig)


df = load_data(SPREADSHEET_ID, SHEET_NAME)
st.write(df)
plot_scatter(df=df, tag_column="ブロック")