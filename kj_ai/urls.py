from django.contrib import admin
from django.urls import include, path
from .views import *


app_name = 'kj_ai'

urlpatterns = [
    path('input_url/', InputUrlView.as_view(), name='input_url'),
    path('result/', ResultView.as_view(), name='result'),
    # path('success/', index, name='success'),
    path('about/', AboutPageView.as_view(), name='about'),
]