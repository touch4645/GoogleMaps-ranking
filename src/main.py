from flask import Flask, render_template, Markup, request, jsonify, json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
app = Flask(__name__)

@app.route('/')
def hello():
    # options
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # # launch driver
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    # # set wait time
    # driver.implicitly_wait(60)

    # song_url = 'https://www.ufret.jp/song.php?data=1194'
    # driver.get(song_url)
    # # 原曲キーに戻る
    # select_element = driver.find_element_by_name('keyselect')
    # select_obj = Select(select_element)
    # select_obj.select_by_value('0')
    # html = driver.page_source
    # driver.quit()
    # # scraping
    # soup = BeautifulSoup(html, 'html.parser')
    # chord_tags = soup.find_all('rt')
    # ans = []
    # for tag in chord_tags:
    #     ans.append(tag.text)
    # return ' '.join(ans)
    return render_template('top.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)