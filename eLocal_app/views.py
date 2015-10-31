from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from .forms import ZipcodeForm, ProductSearchForm, StoreSearchForm, ProductAddForm, StoreAddForm
from .models import Store, Item, Inventory
from .utils import ElocalUtils

def homePage(request):
    if request.method == 'GET':
        form = ZipcodeForm()
    else:
        form = ZipcodeForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            searchForm = StoreSearchForm()
            addProductForm = ProductAddForm()
            addStoreForm = StoreAddForm()
            stores = Store.objects.filter(zip_code=zip_code)
            results = ElocalUtils.parseStoresInfo(stores)
            request.session['zip_code'] = zip_code
            request.session['cart'] = []
            return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'stores': results, 'zip_code': zip_code})
    return render(request, 'eLocal_app/homePage.html', {'form': form})

def productSearchPage(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        searchForm = ProductSearchForm()
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        zip_code = request.session['zip_code']
        stores = Store.objects.filter(zip_code=zip_code)
        results = ElocalUtils.parseProductsInfo(stores, zip_code)
        return render(request, 'eLocal_app/productSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': results, 'zip_code': zip_code})

def storeSearchPage(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        searchForm = StoreSearchForm()
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        zip_code = request.session['zip_code']
        stores = Store.objects.filter(zip_code=zip_code)
        results = ElocalUtils.parseStoresInfo(stores)
        return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'stores': results, 'zip_code': zip_code})

def shoppingPage(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        zip_code = request.session['zip_code']
        results = request.session['cart']
        return render(request, 'eLocal_app/shoppingPage.html', {'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': results, 'zip_code': zip_code})

def addStore(request):
    if request.method == 'POST':
        form = StoreAddForm(request.POST)
        if form.is_valid():
            store_name = form.cleaned_data['store_name']
            address = form.cleaned_data['street_number'] + ' ' + form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            country = form.cleaned_data['country']
            has_card = form.cleaned_data['has_card']
            if not Store.objects.filter(name=store_name, address=address, city=city, state=state, country=country).exists():
                Store.create(store_name, address, city, state, zip_code, country, has_card)
        return HttpResponseRedirect('/stores')

def addProduct(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            description = form.cleaned_data['description']
            price = float(form.cleaned_data['price'])
            store_name = form.cleaned_data['store_name']
            store = Store.objects.get(name=store_name)
            if Item.objects.filter(name=product_name).exists():
                item = Item.objects.get(name=product_name)
            else:
                item = Item.create(product_name, description)
            item.addToStore(store.id, price)
        return HttpResponseRedirect('/products')

def searchProduct(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        searchForm = ProductSearchForm(request.GET)
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        zip_code = request.session['zip_code']
        stores = Store.objects.filter(zip_code=zip_code)
        results = ElocalUtils.parseProductsInfo(stores, zip_code)
        if searchForm.is_valid():
            name = searchForm.cleaned_data['name']
            results = ElocalUtils.searchProduct(name, zip_code)
            if len(results) == 0:
                messages.error(request, 'No matching products.')
        else:
            messages.error(request, 'Must input a product.')
        return render(request, 'eLocal_app/productSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': results, 'zip_code': zip_code})

def searchStore(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        searchForm = StoreSearchForm(request.GET)
        addProductForm = ProductAddForm()
        addStoreForm = StoreAddForm()
        zip_code = request.session['zip_code']
        results = Store.objects.filter(zip_code=zip_code)
        if searchForm.is_valid():
            name = searchForm.cleaned_data['name']
            results = ElocalUtils.searchStore(name, zip_code)
            if len(results) == 0:
                messages.error(request, 'No matching stores.')
        else:
            messages.error(request, 'Must input a store.')
        return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'stores': results, 'zip_code': zip_code})

def addCart(request, product_id, store_id):
    product = Item.objects.get(id=product_id)
    store = Store.objects.get(id=store_id)
    cart_item = ElocalUtils.getInfoFromProductStore(product, store)
    if 'cart' in request.session:
        cart = request.session['cart']
        cart.append(cart_item)
        request.session['cart'] = cart
    return HttpResponseRedirect('/products')
