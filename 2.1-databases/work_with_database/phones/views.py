from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    arg = request.GET.get('sort', None)
    if arg == 'min_price':
        sort = 'price'
    elif arg == 'max_price':
        sort = '-price'
    else:
        sort = 'name'
    phones = Phone.objects.all().order_by(sort)
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug).first()
    context = {'phone': phone}
    return render(request, template, context)
