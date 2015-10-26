from .models import Inventory, Item, Store

class ElocalUtils:
    @staticmethod
    def getAllStores():
        stores = Store.objects.all()
        results = []
        for store in stores:
            result = {'store_name': store.name, 'address': store.address}
            products = Inventory.getItemsForStore(store.id)
            product_list = []
            for product in products:
                price = Inventory.getPrice(store.id, product.id)
                product_list.append((product.name, price))
            result['product_list'] = product_list
            results.append(result)
        return results

    @staticmethod
    def parseSearchStore(name):
        stores = Store.getStores(name)
        results = []
        for store in stores:
            result = {'store_name': store.name}
            products = Inventory.getItemsForStore(store.id)
            product_list = []
            for product in products:
                price = Inventory.getPrice(store.id, product.id)
                product_list.append((product.name, price))
            result['product_list'] = product_list
            results.append(result)
        return results

    @staticmethod
    def getAllProducts():
        products = Item.objects.all()
        results = []
        for product in products:
            stores = Inventory.getStoresForItem(product.id)
            price = Inventory.getPrice(stores[0].id, product.id)
            store_name = stores[0].name
            results.append({'product_name': product.name, 'price': price, 'store_name': store_name})
        return results

    @staticmethod
    def parseSearchProduct(name):
        products = Item.getItems(name)
        results = []
        for product in products:
            stores = Inventory.getStoresForItem(product.id)
            price = Inventory.getPrice(stores[0].id, product.id)
            store_name = stores[0].name
            results.append({'product_name': product.name, 'price': price, 'store_name': store_name})
        return results
