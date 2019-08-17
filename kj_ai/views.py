from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.urls import reverse_lazy
from .forms import *
import os
import pandas as pd
import numpy as np
from key_judge_app.settings import BASE_DIR
import pickle
# UPLOAD_DIR = os.path.join(BASE_DIR, 'static/csv_files')


class InputUrlView(FormView):
    template_name = 'kj_ai/input_url.html'
    form_class = InputUrlForm
    success_url = reverse_lazy('kj_ai:about')

    # def form_valid(self, form):
    #     csv_file = form.cleaned_data['csv_file']
    #     os.makedirs(UPLOAD_DIR, exist_ok=True)
    #     save_path = os.path.join(UPLOAD_DIR, csv_file.name)
    #     with open(save_path, 'wb') as destination:
    #         for chunk in csv_file.chunks():
    #             destination.write(chunk)
    #     return super(SelectCsvView, self).form_valid(form)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class ResultView(TemplateView):
    template_name = 'kj_ai/result.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        model_pkl_dir = os.path.join(BASE_DIR, 'static/model/model.pkl')
        loaded_model = pickle.load(open(model_pkl_dir, 'rb'))



        context['result'] = lst
        context['ans'] = np.argmax(lst)
        return context


class AboutPageView(TemplateView):
    template_name = 'kj_ai/about.html'
