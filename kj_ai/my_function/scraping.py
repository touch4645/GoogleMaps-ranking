from bs4 import BeautifulSoup
import requests
from .music_class import *

def func(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
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
