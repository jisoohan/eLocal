from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ZipcodeForm, ProductSearchForm, StoreSearchForm, ProductAddForm, StoreAddForm

# Create your views here.
def homePage(request):
    if request.method == 'GET':
        form = ZipcodeForm()
    else:
        form = ZipcodeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/products')
    return render(request, 'eLocal_app/homePage.html', {'form': form})

def productSearchPage(request):
    if request.method == 'GET':
        searchForm = ProductSearchForm()
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
    return render(request, 'eLocal_app/productSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm})

def storeSearchPage(request):
    if request.method == 'GET':
        searchForm = StoreSearchForm()
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
    return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm})

def shoppingPage(request):
    if request.method == 'GET':
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
    return render(request, 'eLocal_app/shoppingPage.html', {'addProductForm': addProductForm, 'addStoreForm': addStoreForm})

def addProduct(request):
    if request.method == 'GET':
        form = ProductAddForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['']
    else:
        form = ProductAddForm()
    return render(request, 'eLocal_app/productSearchPage.html', {'form': form})

