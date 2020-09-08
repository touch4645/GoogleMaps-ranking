from flask import Flask, render_template, Markup, request, jsonify, json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
from .music_class import *
app = Flask(__name__)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/link')
def link():
    return render_template('link.html')


def scraping(song_url):
    # options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # launch driver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # set wait time
    driver.implicitly_wait(60)

    driver.get(song_url)
    # 原曲キーに戻す
    select_element = driver.find_element_by_name('keyselect')
    select_obj = Select(select_element)
    select_obj.select_by_value('0')
    html = driver.page_source
    driver.quit()

    ################# scraping
    soup = BeautifulSoup(html, 'html.parser')
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


@app.route('/', methods=['GET', 'POST'])
def top():
    if request.method == 'GET':
        return render_template('top.html')
    if request.method == 'POST':
        url = request.form['url']
        df, song_name = scraping(url)
        return render_template('result.html', song_name=song_name, answer=answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)