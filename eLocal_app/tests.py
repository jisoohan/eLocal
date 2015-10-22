from django.test import TestCase
from eLocal_app.models import Item, Store, Inventory

# Create your tests here.

class InventoryTest(TestCase):
    def testInvalidItemId(self):
        try:
            result = Inventory.getStoresForItem(-1)
            self.fail("Getting stores for invalid item ID should throw exception")
        except Item.DoesNotExist:
            return
     
    def testInvalidStoreId(self):
        try:
            result = Inventory.getItemsForStore(-1)
            self.fail("Getting items for invalid store ID should throw exception")
        except Store.DoesNotExist:
            return
    
class ItemTest(TestCase):
    def testInvalidKeyword(self):
        result = Item.getItems('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with invalid keyword should return 0 results")


class StoreTest(TestCase):
    def testInvalidKeyword(self):
        result = Store.getStores('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with invalid keyword should return 0 results")
    