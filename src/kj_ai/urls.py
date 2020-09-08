from django.contrib import admin
from django.urls import include, path
from .views import *


app_name = 'kj_ai'

urlpatterns = [
    path('', InputUrlView.as_view(), name='input_url'),
    path('result/', ResultView.as_view(), name='result'),
    # path('success/', index, name='success'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('news/', NewsPageView.as_view(), name='news'),
    path('link/', LinkPageView.as_view(), name='link'),
]