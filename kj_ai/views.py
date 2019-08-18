from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import *
import os
import pandas as pd
import numpy as np
from key_judge_app.settings import BASE_DIR
import pickle
from .my_function.scraping import func as scraping

# UPLOAD_DIR = os.path.join(BASE_DIR, 'static/csv_files')


class InputUrlView(FormView):
    template_name = 'kj_ai/input_url.html'
    form_class = InputUrlForm
    # success_url = reverse_lazy('kj_ai:result')

    def form_valid(self, form):
        url = form.cleaned_data['url_str']
        number = url.split('=')[-1]
        return redirect('kj_ai:result',song_id=number)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class ResultView(TemplateView):
    template_name = 'kj_ai/result.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        url = 'https://www.ufret.jp/song.php?data=' + kwargs['song_id']

        # urlから曲のコードカウントしたdfと曲名を抽出
        df, song_name = scraping(url)

        # 学習済みモデルとラベルエンコーダーの読み込み
        model_pkl_dir = os.path.join(BASE_DIR, 'static/model/model.pkl')
        le_pkl_dir = os.path.join(BASE_DIR, 'static/model/le.pkl')
        loaded_model = pickle.load(open(model_pkl_dir, 'rb'))
        le = pickle.load(open(le_pkl_dir, 'rb'))

        # 予測して、結果を文字列に変換
        pred_y_value = loaded_model.predict(df)
        pred_y_label = le.inverse_transform(pred_y_value)[0]
        if pred_y_label.split('_')[-1] == 'Major':
            answer = pred_y_label.split('_')[0]
        else:
            answer = pred_y_label.split('_')[0] + 'm'

        # htmlに結果を渡す
        context['answer'] = answer
        context['song_name'] = song_name
        return context


class AboutPageView(TemplateView):
    template_name = 'kj_ai/about.html'


class NewsPageView(TemplateView):
    template_name = 'kj_ai/news.html'


class LinkPageView(TemplateView):
    template_name = 'kj_ai/link.html'
