from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ZipcodeForm, ProductSearchForm, StoreSearchForm, ProductAddForm, StoreAddForm, ProductUpdateForm, PriceUpdateForm
from .models import Store, Item, Inventory
from .utils import ElocalUtils

def homePage(request):
    if request.method == 'GET':
        form = ZipcodeForm()
    else:
        form = ZipcodeForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            radius = form.cleaned_data['radius']
            coordinates = ElocalUtils.getCoorFromZipcode(zip_code)
            if ElocalUtils.isValidZipcode(zip_code) and len(coordinates) != 0:
                request.session['zip_code'] = zip_code
                request.session['coordinates'] = coordinates
                request.session['radius'] = int(radius)
                request.session['cart'] = []
                request.session['stores'] = ElocalUtils.geolocateStores(request.session['coordinates'], request.session['radius'])
                request.session['products'] = ElocalUtils.geolocateProducts(request.session['stores'])
                searchForm = StoreSearchForm()
                addProductForm = ProductAddForm(request.session['coordinates'], request.session['radius'])
                addStoreForm = StoreAddForm()
                return HttpResponseRedirect('/stores')
            else:
                form.add_error('zip_code', 'Must be a valid zipcode.')
    return render(request, 'eLocal_app/homePage.html', {'form': form})

def productSearchPage(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        zip_code = request.session['zip_code']
        radius = request.session['radius']
        searchForm = ProductSearchForm()
        addProductForm = ProductAddForm(request.session['coordinates'], request.session['radius'])
        addStoreForm = StoreAddForm()
        products = request.session['products']
        editProductForms = []
        editPriceForms = []
        ids = []
        for product in products:
            editProductForm = ProductUpdateForm(initial={'product_name': product['name'],'description': product['description']})
            editProductForms.append((product['id'], editProductForm))
            for store in product['store_list']:
                editPriceForm = PriceUpdateForm(initial={'price': store['price']})
                editPriceForms.append([product['id'], store['id'], editPriceForm])
                ids.append([product['id'], store['id']])
        return render(request, 'eLocal_app/productSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': products, 'editProductForms': editProductForms, 'editPriceForms': editPriceForms, 'ids': ids, 'zip_code': zip_code, 'radius': radius})

def storeSearchPage(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        zip_code = request.session['zip_code']
        radius = request.session['radius']
        searchForm = StoreSearchForm()
        addProductForm = ProductAddForm(request.session['coordinates'], request.session['radius'])
        addStoreForm = StoreAddForm()
        stores = request.session['stores']
        editStoreForms = []
        editPriceForms = []
        ids = []
        for store in stores:
            editStoreForm = StoreAddForm(initial={
                                         'store_name': store['name'],
                                         'street_number': store['address'].split()[0],
                                         'street_address': ' '.join(store['address'].split()[1:]),
                                         'city': store['city'],
                                         'state': store['state'],
                                         'zip_code': store['zip_code'],
                                         'country': store['country'],
                                         'has_card': store['has_card']
                                         })
            editStoreForms.append((store['id'], editStoreForm))
            for product in store['product_list']:
                editPriceForm = PriceUpdateForm(initial={'price': product['price']})
                editPriceForms.append([product['id'], store['id'], editPriceForm])
                ids.append([product['id'], store['id']])
        return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'stores': stores, 'editStoreForms': editStoreForms, 'editPriceForms': editPriceForms, 'ids': ids, 'zip_code': zip_code, 'radius': radius})

def shoppingPage(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        zip_code = request.session['zip_code']
        radius = request.session['radius']
        addProductForm = ProductAddForm(request.session['coordinates'], request.session['radius'])
        addStoreForm = StoreAddForm()
        results = request.session['cart']
        return render(request, 'eLocal_app/shoppingPage.html', {'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': results, 'zip_code': zip_code, 'radius': radius})

def updateStore(request, store_id):
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
            store = Store.objects.get(id=store_id)
            if Store.updateStoreCheck(store, store_name, address, city, state, zip_code, country, has_card):
                coordinates = ElocalUtils.getCoorFromAddress(address, city, state, zip_code, country)
                Store.objects.filter(id=store_id).update(name=store_name, address=address, city=city, state=state, zip_code=zip_code, country=country, has_card=has_card, latitude=coordinates[0], longitude=coordinates[1])
                request.session['stores'] = ElocalUtils.geolocateStores(request.session['coordinates'], request.session['radius'])
                request.session['products'] = ElocalUtils.geolocateProducts(request.session['stores'])
                cart = request.session['cart']
                request.session['cart'] = ElocalUtils.updateCartStore(cart, Store.objects.get(id=store_id))
        return HttpResponseRedirect('/stores')

def updateProduct(request, product_id):
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            description = form.cleaned_data['description']
            product = Item.objects.get(id=product_id)
            product_list = request.session['products']
            if Item.updateProductCheck(product, product_list, product_name, description):
                Item.objects.filter(id=product_id).update(name=product_name, description=description)
                request.session['stores'] = ElocalUtils.geolocateStores(request.session['coordinates'], request.session['radius'])
                request.session['products'] = ElocalUtils.geolocateProducts(request.session['stores'])
                cart = request.session['cart']
                request.session['cart'] = ElocalUtils.updateCartProduct(cart, Item.objects.get(id=product_id))
        return HttpResponseRedirect('/stores')

def updatePrice(request, product_id, store_id):
    if request.method == 'POST':
        form = PriceUpdateForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            if price != Inventory.getPrice(store_id, product_id):
                Inventory.objects.filter(store=Store.objects.get(id=store_id), item=Item.objects.get(id=product_id)).update(price=price)
                request.session['stores'] = ElocalUtils.geolocateStores(request.session['coordinates'], request.session['radius'])
                request.session['products'] = ElocalUtils.geolocateProducts(request.session['stores'])
                cart = request.session['cart']
                request.session['cart'] = ElocalUtils.updateCartPrice(cart, product_id, store_id, price)
        return HttpResponseRedirect('/stores')

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
            if not Store.hasDuplicate(store_name, address, city, state, zip_code, country, has_card):
                coordinates = ElocalUtils.getCoorFromAddress(address, city, state, zip_code, country)
                store = Store.create(store_name, address, city, state, zip_code, country, has_card, coordinates[0], coordinates[1])
                if ElocalUtils.checkDistance(request.session['coordinates'], [(store.latitude, store.longitude)], request.session['radius']):
                    store_list = request.session['stores']
                    store_list.append(ElocalUtils.parseStore(store))
                    request.session['stores'] = store_list
        return HttpResponseRedirect('/stores')

def addProduct(request):
    if request.method == 'POST':
        zip_code = request.session['zip_code']
        form = ProductAddForm(request.session['coordinates'], request.session['radius'], request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            description = form.cleaned_data['description']
            price = float(form.cleaned_data['price'])
            store_id = form.cleaned_data['store_name']
            if not Inventory.hasDuplicateItem(product_name, store_id):
                product_list = request.session['products']
                item = ElocalUtils.getProductFromSession(product_name, product_list)
                if item is None:
                    item = Item.create(product_name, description)
                item.addToStore(store_id, price)
                request.session['stores'] = ElocalUtils.geolocateStores(request.session['coordinates'], request.session['radius'])
                request.session['products'] = ElocalUtils.geolocateProducts(request.session['stores'])
        return HttpResponseRedirect('/products')

def deleteProductFromStore(request, product_id, store_id):
    product = Item.objects.get(id=product_id)
    Inventory.objects.filter(store=Store.objects.get(id=store_id), item=product).delete()
    if len(product.store_set.all()) == 0:
        product.delete()
    request.session['stores'] = ElocalUtils.geolocateStores(request.session['coordinates'], request.session['radius'])
    request.session['products'] = ElocalUtils.geolocateProducts(request.session['stores'])
    cart = request.session['cart']
    request.session['cart'] = ElocalUtils.deleteCartProductFromStore(cart, product_id, store_id)
    return HttpResponseRedirect('/stores')

def deleteStore(request, store_id):
    store = Store.objects.get(id=store_id)
    products = Inventory.getItemsForStore(store_id)
    for product in products:
        Inventory.objects.filter(store=store, item=product).delete()
        if len(product.store_set.all()) == 0:
            product.delete()
    store.delete()
    request.session['stores'] = ElocalUtils.geolocateStores(request.session['coordinates'], request.session['radius'])
    request.session['products'] = ElocalUtils.geolocateProducts(request.session['stores'])
    cart = request.session['cart']
    request.session['cart'] = ElocalUtils.deleteCartStore(cart, store_id)
    return HttpResponseRedirect('/stores')

def searchProduct(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        zip_code = request.session['zip_code']
        radius = request.session['radius']
        searchForm = ProductSearchForm(request.GET)
        addProductForm = ProductAddForm(request.session['coordinates'], request.session['radius'])
        addStoreForm = StoreAddForm()
        products = request.session['products']
        editProductForms = []
        editPriceForms = []
        ids = []
        if searchForm.is_valid():
            name = searchForm.cleaned_data['name']
            products = ElocalUtils.searchProduct(name, products)
            if len(products) == 0:
                messages.error(request, 'No matching products.')
        else:
            messages.error(request, 'Must input a product.')
        for product in products:
            editProductForm = ProductUpdateForm(initial={'product_name': product['name'],'description': product['description']})
            editProductForms.append((product['id'], editProductForm))
            for store in product['store_list']:
                editPriceForm = PriceUpdateForm(initial={'price': store['price']})
                editPriceForms.append([product['id'], store['id'], editPriceForm])
                ids.append([product['id'], store['id']])
        return render(request, 'eLocal_app/productSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'products': products, 'editProductForms': editProductForms, 'editPriceForms': editPriceForms, 'ids': ids, 'zip_code': zip_code, 'radius': radius})

def searchStore(request):
    if request.method == 'GET':
        if 'zip_code' not in request.session:
            return HttpResponseRedirect('/')
        zip_code = request.session['zip_code']
        radius = request.session['radius']
        searchForm = StoreSearchForm(request.GET)
        addProductForm = ProductAddForm(request.session['coordinates'], request.session['radius'])
        addStoreForm = StoreAddForm()
        stores = request.session['stores']
        editStoreForms = []
        editPriceForms = []
        ids = []
        if searchForm.is_valid():
            name = searchForm.cleaned_data['name']
            stores = ElocalUtils.searchStore(name, stores)
            if len(stores) == 0:
                messages.error(request, 'No matching stores.')
        else:
            messages.error(request, 'Must input a store.')
        for store in stores:
            editStoreForm = StoreAddForm(initial={
                                         'store_name': store['name'],
                                         'street_number': store['address'].split()[0],
                                         'street_address': ' '.join(store['address'].split()[1:]),
                                         'city': store['city'],
                                         'state': store['state'],
                                         'zip_code': store['zip_code'],
                                         'country': store['country'],
                                         'has_card': store['has_card']
                                         })
            editStoreForms.append((store['id'], editStoreForm))
            for product in store['product_list']:
                editPriceForm = PriceUpdateForm(initial={'price': product['price']})
                editPriceForms.append([product['id'], store['id'], editPriceForm])
                ids.append([product['id'], store['id']])
        return render(request, 'eLocal_app/storeSearchPage.html', {'searchForm': searchForm, 'addProductForm': addProductForm, 'addStoreForm': addStoreForm, 'stores': stores, 'editStoreForms': editStoreForms, 'editPriceForms': editPriceForms, 'ids': ids, 'zip_code': zip_code, 'radius': radius})

def addCart(request, product_id, store_id):
    if 'cart' in request.session:
        hashCode = ElocalUtils.getHash(product_id, store_id)
        cart = request.session['cart']
        updated_cart = ElocalUtils.addCart(hashCode, cart)
        if updated_cart is not None:
            cart = updated_cart
        else:
            product = Item.objects.get(id=product_id)
            store = Store.objects.get(id=store_id)
            cart_item = ElocalUtils.getInfoFromProductStore(product, store)
            cart.append(cart_item)
        request.session['cart'] = cart
    return HttpResponseRedirect('/cart')

def removeCart(request, product_id, store_id):
    if 'cart' in request.session:
        hashCode = ElocalUtils.getHash(product_id, store_id)
        cart = request.session['cart']
        updated_cart = ElocalUtils.removeCart(hashCode, cart)
        request.session['cart'] = updated_cart
    return HttpResponseRedirect('/cart')
