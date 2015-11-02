from .models import Inventory, Item, Store
from django.forms.models import model_to_dict
from operator import itemgetter

class ElocalUtils:

    @staticmethod
    def getStoreChoices(zip_code):
        stores = Store.objects.filter(zip_code=zip_code)
        results = []
        for store in stores:
            results.append((store.id, store.name))
        return results

    @staticmethod
    def parseStoresInfo(stores):
        results = []
        for store in stores:
            store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
            products = Inventory.getItemsForStore(store.id)
            product_list = []
            for product in products:
                price = Inventory.getPrice(store.id, product.id)
                product_dict = model_to_dict(product, fields=[field.name for field in product._meta.fields])
                product_dict['price'] = price
                product_list.append(product_dict)
            sorted_product_list = sorted(product_list, key=itemgetter('price'))
            store_dict['product_list'] = sorted_product_list
            results.append(store_dict)
        return results

    @staticmethod
    def searchStore(name, zip_code):
        stores = [store for store in Store.getStores(name) if store.zip_code == zip_code]
        return ElocalUtils.parseStoresInfo(stores)

    @staticmethod
    def parseProductsInfo(stores, zip_code):
        seen_products = set()
        results = []
        for store in stores:
            products = Inventory.getItemsForStore(store.id)
            for product in products:
                if product.id not in seen_products:
                    seen_products.add(product.id)
                    product_dict = model_to_dict(product, fields=[field.name for field in product._meta.fields])
                    stores = Inventory.getStoresForItem(product.id)
                    store_list = []
                    for store in stores:
                        if store.zip_code == zip_code:
                            store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
                            price = Inventory.getPrice(store.id, product.id)
                            store_dict['price'] = price
                            store_list.append(store_dict)
                    sorted_store_list = sorted(store_list, key=itemgetter('price'))
                    product_dict['store_list'] = sorted_store_list
                    results.append(product_dict)
        return results

    @staticmethod
    def searchProduct(name, zip_code):
        seen_products = set()
        stores = Store.objects.filter(zip_code=zip_code)
        results = []
        for store in stores:
            products = Inventory.getItemsForStore(store.id)
            for product in products:
                if product.id not in seen_products:
                    if name.lower() in product.name.lower():
                        seen_products.add(product.id)
                        product_dict = model_to_dict(product, fields=[field.name for field in product._meta.fields])
                        stores = Inventory.getStoresForItem(product.id)
                        store_list = []
                        for store in stores:
                            if store.zip_code == zip_code:
                                store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
                                price = Inventory.getPrice(store.id, product.id)
                                store_dict['price'] = price
                                store_list.append(store_dict)
                        product_dict['store_list'] = store_list
                        results.append(product_dict)
        return results

    @staticmethod
    def getInfoFromProductStore(product, store):
        price = Inventory.getPrice(store.id, product.id)
        product_dict = model_to_dict(product, fields=[field.name for field in product._meta.fields])
        store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
        return {'product': product_dict, 'store': store_dict, 'price': price, 'quantity': 1}

    @staticmethod
    def getHash(product_id, store_id):
        hashCode = str(product_id) + str(store_id)
        return hashCode

    @staticmethod
    def addCart(hashCode, old_cart):
        found = False
        cart = old_cart
        for item in cart:
            item_hash = ElocalUtils.getHash(item['product']['id'], item['store']['id'])
            if hashCode == item_hash:
                item['quantity'] = item['quantity'] + 1
                found = True
        if found:
            return cart
        else:
            return None

    @staticmethod
    def removeCart(hashCode, old_cart):
        cart = old_cart
        count = 0
        for item in cart:
            item_hash = ElocalUtils.getHash(item['product']['id'], item['store']['id'])
            if hashCode == item_hash:
                if item['quantity'] > 1:
                    item['quantity'] = item['quantity'] - 1
                else:
                    cart.remove(item)
        return cart

    @staticmethod
    def getProductFromZipcode(product_name, zip_code):
        stores = Store.objects.filter(zip_code=zip_code)
        for store in stores:
            products = Inventory.getItemsForStore(store.id)
            for product in products:
                if product_name.lower() == product.name.lower():
                    return Item.objects.get(id=product.id)
        return None

