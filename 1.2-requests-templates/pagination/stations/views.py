from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
import csv


with open(settings.BUS_STATION_CSV, encoding='utf-8') as f:
    bus_dict = list(csv.DictReader(f))


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page = request.GET.get('page', 1)
    values = Paginator(bus_dict, 10)
    pages = values.get_page(page)
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    context = {
         'bus_stations': pages,
         'page': pages,
    }
    return render(request, 'stations/index.html', context)
