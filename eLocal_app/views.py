from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ZipcodeForm, ProductSearchForm, StoreSearchForm

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
        form = ProductSearchForm()
    return render(request, 'eLocal_app/productSearchPage.html', {'form': form})

def storeSearchPage(request):
    if request.method == 'GET':
        form = StoreSearchForm()
    return render(request, 'eLocal_app/storeSearchPage.html', {'form': form})

def shoppingPage(request):
    return render(request, 'eLocal_app/shoppingPage.html')

def addItemPage(request):
    return render(request, 'eLocal_app/addItemPage.html')
