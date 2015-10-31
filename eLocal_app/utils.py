from .models import Inventory, Item, Store
from django.forms.models import model_to_dict

class ElocalUtils:

    @staticmethod
    def getStoreChoices():
        stores = Store.objects.all()
        results = []
        for store in stores:
            results.append((store.name, store.name))
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
            store_dict['product_list'] = product_list
            results.append(store_dict)
        return results

    @staticmethod
    def searchStore(name, zip_code):
        stores = [store for store in Store.getStores(name) if store.zip_code == zip_code]
        results = []
        for store in stores:
            result = {'name': store.name, 'address': store.address, 'city': store.city, 'state': store.state, 'zip_code': store.zip_code, 'country': store.country, 'has_card': store.has_card}
            products = Inventory.getItemsForStore(store.id)
            product_list = []
            for product in products:
                price = Inventory.getPrice(store.id, product.id)
                product_list.append((product.name, price))
            result['product_list'] = product_list
            results.append(result)
        return results

    @staticmethod
    def parseProductsInfo(stores):
        results = []
        for store in stores:
            products = Inventory.getItemsForStore(store.id)
            for product in products:
                product_dict = model_to_dict(product, fields=[field.name for field in product._meta.fields])
                stores = Inventory.getStoresForItem(product.id)
                store_list = []
                for store in stores:
                    store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
                    price = Inventory.getPrice(store.id, product.id)
                    store_dict['price'] = price
                    store_list.append(store_dict)
                product_dict['store_list'] = store_list
                results.append(product_dict)
        return results

    @staticmethod
    def searchProduct(name, zip_code):
        stores = Store.objects.filter(zip_code=zip_code)
        products = []
        results = []
        for store in stores:
            products = Inventory.getItemsForStore(store.id)
            for product in products:
                if name in product.name:
                    result = {'product_name': product.name, 'description': product.description}
                    stores = Inventory.getStoresForItem(product.id)
                    store_list = []
                    for store in stores:
                        price = Inventory.getPrice(store.id, product.id)
                        store_list.append((store.name, price))
                    result['store_list'] = store_list
                    results.append(result)
        return results

