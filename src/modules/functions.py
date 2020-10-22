# -*- coding: utf-8 -*-
from pytrends.request import TrendReq

#seleniumとbeautifulsoupをインポートimport time
from bs4 import BeautifulSoup
from selenium import webdriver  # Webブラウザを自動操作する（python -m pip install selenium)
from selenium.webdriver.chrome.options import Options  # オプションを使うために必要

import requests
import time

# 初期化
from itertools import zip_longest
from itertools import filterfalse


def get_keyword_relation(keyword='名古屋 ディナー'):
    # キーワードリスト
    kw_list = [keyword]

    # GoogleTrandsのリスト
    google_trend_list = []

    """
    期間の指定例：
    timeframe='now 1-d' -> 過去1日間（あるいは7-dで指定）
    timeframe='today 1-m' -> 過去1ヶ月間（あるいは3-mで指定）
    timeframe='today 5-y' -> 過去5年間（5-yしか指定できない）
    """
    pytrends = TrendReq(hl='ja-JP', tz=360)
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='JP', gprop='')
    trends = pytrends.related_queries()
    trends_values = trends[keyword]['top'].values.tolist()

    return trends_values

    # for value in trends_values:
    #     item = str(value[0]).strip(keyword)
    #     item = item.replace('　', '')
    #     item = item.replace(' ', '')
    #     google_trend_list.append(item)
    #
    # print('google_trend_list = ' + str(google_trend_list))


def get_lat_lon_from_address(address):
    """
    address_lにlistの形で住所を入れてあげると、latlonsという入れ子上のリストで緯度経度のリストを返す関数。
    >>>>get_lat_lon_from_address(['東京都文京区本郷7-3-1','東京都文京区湯島３丁目３０−１'])
    [['35.712056', '139.762775'], ['35.707771', '139.768205']]
    """
    url = 'http://www.geocoding.jp/api/'
    latlons = []

    payload = {"v": 1.1, 'q': address}
    r = requests.get(url, params=payload)
    ret = BeautifulSoup(r.content, 'lxml')
    if ret.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    else:
        lat = ret.find('lat').string
        lon = ret.find('lng').string
        latlons.append([lat, lon])
        time.sleep(10)
    return latlons


def get_local_ranking(keys, address):
    # options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # launch driver
    driver = webdriver.Chrome(chrome_options=chrome_options)

    lat = get_lat_lon_from_address(address)

    #Google mapsを開く
    url = 'https://www.google.co.jp/maps/@' + lat[0][0] + ','+ lat[0][1] +',14z'
    driver.get(url)

    time.sleep(5)

    #データ入力
    id = driver.find_element_by_id("searchboxinput")
    id.send_keys(keys)

    time.sleep(1)

    #クリック
    search_button = driver.find_element_by_xpath("//*[@id='searchbox-searchbutton']")
    search_button.click()

    time.sleep(3)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    titles = soup.find_all(class_="section-result-title")
    rates = soup.find_all(class_="cards-rating-score")
    reviews = soup.find_all(class_="section-result-num-ratings")
    details = soup.find_all(class_="section-result-details")
    addresses = soup.find_all(class_="section-result-location")

    n = 1
    result = {}

    for title, rate, review, detail, address in zip(titles, rates, reviews, details, addresses):
        local = {}
        local["title"] = title.text.strip()
        local['rate'] = rate.text.strip()
        local['review'] = review.text.strip()
        local['detail'] = detail.text.strip()
        local['address'] = address.text.strip()
        result[n] = local
        n += 1

    return result
    driver.close()


def searchTrends():
    pytrends = TrendReq(hl='ja-JP', tz=360)

    # キーワードリスト
    kw_list = []
    # 主キーワード
    primary_kw = input("基準キーワード：")

    kw = input("キーワード：")

    while kw != "end":
        kw_list.append(kw)
        kw = input("キーワード(入力を終了する場合はendを入力)：")


    group_by = 4
    chunks = zip_longest(*[iter(kw_list)]*group_by)
    p = lambda x: x is None

    merged_df = None
    for elems in list(chunks):
        elems = list(filterfalse(p, elems))
        elems.append(primary_kw)
        pytrends.build_payload(elems, cat=0, timeframe='today 12-m', geo='JP', gprop='')
        df = pytrends.interest_over_time()
        # 取得結果のスコアは String になる。 float 変換したいので、True/False が設定されている `isPartial` を削除して float に変換する。
        del df['isPartial']
        df = df.astype('float64')
        # dataframe　を primary_kw で最大値で正規化する
        scaled_dataframe = df.div(df[primary_kw].max(), axis=0)
        if merged_df is None:
            merged_df = scaled_dataframe
        else:
            # ValueError: columns overlap but no suffix specified が発生するので、やむなく、'postgresql' を削除
            del scaled_dataframe[primary_kw]
            merged_df = merged_df.join(scaled_dataframe)

    # Dataframe を表示
    merged_df

    # %matplotlib inline

    mpl.rcParams['font.family'] = 'Hiragino Maru Gothic Pro'
    # 数が多すぎるので出力対象を絞りこむ
    kw_list.append(primary_kw)
    #keyword_list = ['Mezzanine','postgresql','React','JavaScript','Python']
    merged_df[kw_list].plot(logy=True, figsize=(15, 6))

if __name__ == "__main__":
    print(get_local_ranking('名古屋　居酒屋', '名古屋市'))
    pass