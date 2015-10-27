from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ZipcodeForm, ProductSearchForm, StoreSearchForm, ProductAddForm, StoreAddForm
from .models import Store, Item, Inventory
from .utils import ElocalUtils

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
        results = ElocalUtils.getAllProducts()
    return render(request, 'eLocal_app/productSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': results})

def storeSearchPage(request):
    if request.method == 'GET':
        searchForm = StoreSearchForm()
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        stores = Store.objects.all()
        results = ElocalUtils.getAllStores()
    return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'stores': results})

def shoppingPage(request):
    if request.method == 'GET':
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
    return render(request, 'eLocal_app/shoppingPage.html', {'addProductForm': addProductForm, 'addStoreForm': addStoreForm})

def addStore(request):
    if request.method == 'POST':
        form = StoreAddForm(request.POST)
        if form.is_valid():
            store_name = form.cleaned_data['store_name']
            address = form.cleaned_data['address']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            Store.create(store_name, address, latitude, longitude)
        return HttpResponseRedirect('/stores')

def addProduct(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            price = float(form.cleaned_data['price'])
            store_name = form.cleaned_data['store_name']
            store_list = Store.getStores(store_name)
            if len(store_list) == 0:
                messages.error(request, 'Store must exist.')
                return HttpResponseRedirect('/products')
            if Item.objects.filter(name=product_name).exists():
                item = Item.objects.get(name=product_name)
            else:
                item = Item.create(product_name)
            item.addToStore(store_list[0].id, price)
        return HttpResponseRedirect('/products')

def searchProduct(request):
    if request.method == 'GET':
        searchForm = ProductSearchForm(request.GET)
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        results = []
        if searchForm.is_valid():
            name = searchForm.cleaned_data['name']
            results = ElocalUtils.parseSearchProduct(name)
            if len(results) == 0:
                messages.error(request, 'No matching products.')
                results = ElocalUtils.getAllProducts()
        else:
            messages.error(request, 'Must input a product.')
            results = ElocalUtils.getAllProducts()
        return render(request, 'eLocal_app/productSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': results})

def searchStore(request):
    if request.method == 'GET':
        searchForm = StoreSearchForm(request.GET)
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        if searchForm.is_valid():
            name = searchForm.cleaned_data['name']
            results = ElocalUtils.parseSearchStore(name)
            if len(results) == 0:
                messages.error(request, 'No matching stores.')
                results = ElocalUtils.getAllStores()
        else:
            messages.error(request, 'Must input a store.')
            results = ElocalUtils.getAllStores()
        return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'stores': results})
