from django.contrib import admin
from django.urls import path

from config.api import btc_usd, history, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home),
    path("btcrate/", btc_usd),
    path("history/", history),
]
