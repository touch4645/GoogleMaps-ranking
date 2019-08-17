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
        df, song_name = scraping(url)
        model_pkl_dir = os.path.join(BASE_DIR, 'static/model/model.pkl')
        le_pkl_dir = os.path.join(BASE_DIR, 'static/model/le.pkl')
        loaded_model = pickle.load(open(model_pkl_dir, 'rb'))
        le = pickle.load(open(le_pkl_dir, 'rb'))
        pred_y = loaded_model.predict(df)
        context['answer'] = pred_y
        context['song_name'] = song_name
        return context


class AboutPageView(TemplateView):
    template_name = 'kj_ai/about.html'
