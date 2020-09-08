import pickle
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
from .music_class import *


def get_soup(song_url):
    """
    song_url: ufretの曲url
    seleniumで原曲キーに戻す→html取得→soupにする
    """
    # options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # launch driver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # set wait time
    driver.implicitly_wait(60)

    # open
    driver.get(song_url)
    # 原曲キーに戻す
    select_element = driver.find_element_by_name('keyselect')
    select_obj = Select(select_element)
    select_obj.select_by_value('0')
    html = driver.page_source
    # quit
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    return soup


def scraping(soup):
    # 曲名取得
    song_name = soup.find('title').text.split('ギ')[0]
    song_name = song_name[:len(song_name) - 1]

    # Songインスタンス作成
    song = Song(song_name, Chord('C'))

    # コードを読み取る
    chord_lst = soup.find_all('rt')
    for c in chord_lst:
        chord_str = c.text
        if c.text[0] == 'N':
            continue
        chord = Chord(chord_str)
        song.append_chord(chord)

    df = song.to_DataFrame()
    df = df[df.columns[2:]]
    for col in df.columns:
        df[col] = df[col].astype(float)

    return df, song_name

def sort_proba(proba, le):
    # classのMajor minorの表記を変更する
    class_names = []
    for c in le.classes_:
        if c.split('_')[-1] == 'Major':
            class_names.append(c.split('_')[0])
        else:
            class_names.append(c.split('_')[0] + 'm')

    # 確率とクラス名のdfを作って 確率の降順でソート 上位5つをreturn
    key_proba_df = pd.DataFrame({'proba': proba*100, 'key': class_names})
    key_proba_df = key_proba_df.sort_values('proba', ascending=False)[:5]

    return key_proba_df


def predict(df):
    # 学習済みモデルとラベルエンコーダーの読み込み
    model_pkl_dir = 'static/model/model.pkl'
    le_pkl_dir = 'static/model/le.pkl'
    loaded_model = pickle.load(open(model_pkl_dir, 'rb'))
    le = pickle.load(open(le_pkl_dir, 'rb'))

    # 予測して、結果を文字列に変換
    proba = loaded_model.predict_proba(df)
    top5_df = sort_proba(proba[0], le)
    answer = top5_df.iloc[0, 1]

    return top5_df, answer


def judge_key(song_url):
    soup = get_soup(song_url)
    df, song_name = scraping(soup)
    top5_df, answer = predict(df)

    context = {}
    context['answer'] = answer
    context['song_name'] = song_name
    context['top5_df'] = top5_df

    return context




