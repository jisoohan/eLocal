from .models import Inventory, Item, Store
from django.forms.models import model_to_dict
from operator import itemgetter
import googlemaps

class ElocalUtils:

    @staticmethod
    def getCoorFromZipcode(zip_code):
        client = googlemaps.Client(key='AIzaSyBuEhmVjHKmjRSodKx3dYUqbyCFquSDMWc')
        location = client.geocode(components={'postal_code': zip_code, 'country': 'US'})
        if len(location) == 0:
            origin = []
        else:
            origin = [(location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])]
        return origin

    @staticmethod
    def checkDistance(origin, destination, radius):
        client = googlemaps.Client(key='AIzaSyBuEhmVjHKmjRSodKx3dYUqbyCFquSDMWc')
        dis_matrix = client.distance_matrix(origin, destination, units="imperial")
        distance = 0.00062137 * dis_matrix['rows'][0]['elements'][0]['distance']['value']
        if distance <= radius:
            return True
        return False

    @staticmethod
    def isValidZipcode(zip_code):
        client = googlemaps.Client(key='AIzaSyBuEhmVjHKmjRSodKx3dYUqbyCFquSDMWc')
        location = client.geocode(components={'postal_code': zip_code})
        if len(location) == 0:
            return False
        else:
            return True

    @staticmethod
    def geolocateStores(origin, radius):
        stores = Store.objects.all()
        results = []
        for store in stores:
            destination = [(store.latitude, store.longitude)]
            if ElocalUtils.checkDistance(origin, destination, radius):
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
    def geolocateProducts(origin, radius):
        stores = Store.objects.all()
        store_results = []
        for store in stores:
            destination = [(store.latitude, store.longitude)]
            if ElocalUtils.checkDistance(origin, destination, radius):
                store_results.append(store)

        seen_products = set()
        results = []
        for store in store_results:
            products = Inventory.getItemsForStore(store.id)
            for product in products:
                if product.id not in seen_products:
                    seen_products.add(product.id)
                    product_dict = model_to_dict(product, fields=[field.name for field in product._meta.fields])
                    stores = Inventory.getStoresForItem(product.id)
                    store_list = []
                    for store in stores:
                        destination = [(store.latitude, store.longitude)]
                        if ElocalUtils.checkDistance(origin, destination, radius):
                            store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
                            price = Inventory.getPrice(store.id, product.id)
                            store_dict['price'] = price
                            store_list.append(store_dict)
                    sorted_store_list = sorted(store_list, key=itemgetter('price'))
                    product_dict['store_list'] = sorted_store_list
                    results.append(product_dict)
        return results

    @staticmethod
    def getCoorFromAddress(address, city, state, zip_code, country):
        client = googlemaps.Client(key='AIzaSyBuEhmVjHKmjRSodKx3dYUqbyCFquSDMWc')
        location = client.geocode(address + ', ' + city + ', ' + state + ', ' + zip_code + ', ' + country)
        coordinates = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
        return coordinates

    @staticmethod
    def getStoreChoices(origin, radius):
        stores = Store.objects.all()
        results = []
        for store in stores:
            destination = [(store.latitude, store.longitude)]
            if ElocalUtils.checkDistance(origin, destination, radius):
                results.append((store.id, store.name))
        return results

    @staticmethod
    def parseStore(store):
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
        return store_dict

    @staticmethod
    def parseProduct(product):
        product_dict = model_to_dict(product, fields=[field.name for field in product._meta.fields])
        stores = Inventory.getStoresForItem(product.id)
        store_list = []
        for store in stores:
            store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
            price = Inventory.getPrice(store.id, product.id)
            store_dict['price'] = price
            store_list.append(store_dict)
        sorted_store_list = sorted(store_list, key=itemgetter('price'))
        product_dict['store_list'] = sorted_store_list
        return product_dict

    @staticmethod
    def parseProductAddStore(product_list, product, store_id, price):
        results = product_list
        for p in results:
            if p['id'] == product.id:
                store_list = p['store_list']
                store = Store.objects.get(id=store_id)
                store_dict = model_to_dict(store, fields=[field.name for field in store._meta.fields])
                store_dict['price'] = price
                store_list.append(store_dict)
                sorted_store_list = sorted(store_list, key=itemgetter('price'))
                p['store_list'] = sorted_store_list
        return results

    @staticmethod
    def searchStore(name, stores):
        results = []
        for store in stores:
            if name.lower() in store['name'].lower():
                results.append(store)
        return results

    @staticmethod
    def searchProduct(name, products):
        results = []
        for product in products:
            if name.lower() in product['name'].lower():
                results.append(product)
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
    def getProductFromSession(product_name, products):
        for product in products:
            if product_name.lower() == product['name'].lower():
                return Item.objects.get(id=product['id'])
        return None
