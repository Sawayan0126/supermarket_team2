

import streamlit as st
import pandas as pd
import math
import datetime as dt

# 商品情報のデータフレーム
product_code = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
product_name = ["りんご", "みかん", "ぶどう", "のり弁", "しゃけ弁", "タバコ", "メンソールタバコ", "ライター", "お茶", "コーヒー"]
price = [100, 40, 150, 350, 400, 420, 440, 100, 80, 100]
df = pd.DataFrame({"product_code":product_code,
                   "product_name":product_name,
                   "price":price})


def Buy10(df=df, tax=1.08):
    cd=[]
    n=[]
    nn=[]
    x=1
    lighter_count=0
    bentou_count=0
    drink_count=0
    apple_count=0
    tobacco_count=0

    sum=0
    for i in range(len(df)):
        num = st.sidebar.number_input(df.iloc[i][1], 0)
        n.append(num)
        cd.append(df.iloc[i][0])

        if cd[i] in (6,7):  # タバコは税をつけない
            sum += df.loc[df['product_code']==cd[i],'price'].values[0] * n[i]
        else:
            sum += df.loc[df['product_code']==cd[i],'price'].values[0]*tax * n[i]

    for i in range(len(cd)):
        nn.append( n[i] // 11 * 10 + n[i] % 11 ) #11個を10個で計算
        if cd[i] in (6,7):  
            tobacco_count += n[i]    #タバコの個数を数える
        elif cd[i] == 1:            #りんごの個数を数える
            apple_count += n[i]
        elif cd[i] in (4,5):        #弁当の個数を数える
            bentou_count += n[i]
        elif cd[i] in (9,10):       #飲み物の個数を数える
            drink_count += n[i]

    for i in range(len(cd)):    #割引していくぅ！！
        waribiki_11 = (n[i] - nn[i]) * df.loc[df['product_code']==cd[i],'price'].values[0] * tax
        if cd[i] == 1:  #りんごの割引額の高い方を採用
            waribiki_apple = (300-280)*tax*(apple_count//3)       #りんご3個につき20円引き 
            waribiki = max(waribiki_11, waribiki_apple)
        elif cd[i] == 8:  #ライターの割引額の高い方を採用
            waribiki_lighter = df.loc[df['product_code']==cd[i],'price'].values[0] * (tobacco_count//10) * tax 
            waribiki = max(waribiki_11, waribiki_lighter)
        elif cd[i] in (4,5):  #弁当の割引額の高い方を採用
            waribiki_bentou = 20*min(bentou_count, drink_count)    #弁当と飲み物の割引
            waribiki = max(waribiki_11, waribiki_bentou)
        else:       #他の商品は11個買ったら10個になる割引採用
            waribiki=waribiki_11
        sum = sum -waribiki
    return int(sum)

st.title("商品購入シミュレータ")
st.subheader("商品リスト")
st.dataframe(df)
st.sidebar.write("各商品の購入個数を選択してください。")

total_price = Buy10(df=df)

st.subheader("合計金額")
st.write(f"{total_price} 円")
