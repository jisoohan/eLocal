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
    def setUp(self):
        Item.objects.all().delete()
        
    
    def testInvalidKeyword(self):
        result = Item.getItems('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with invalid keyword should return 0 results")
    
    def testSearchItem(self):
        item1 = Item(name="Test item 1")
        item1.save()
        item2 = Item(name="Another thing")
        item2.save()
        item3 = Item(name="Third item")
        item3.save()
        self.assertEqual("Test item 1", item1.name, "Item name is not correctly stored")
        search_1 = Item.getItems("Test item 1")
        self.assertEqual(len(search_1), 1, "Item keyword search with full string should return one item")
        self.assertEqual(item1.id, search_1[0].id, "Item keyword search returned irrelevant item")
        search_2 = Item.getItems("iTeM 1")
        self.assertEqual(len(search_2), 1, "Item keyword search should be case-insensitive and should return one item")
        self.assertEqual(item1.id, search_2[0].id, "Item keyword search returned irrelevant item")
        

class StoreTest(TestCase):
    def testInvalidKeyword(self):
        result = Store.getStores('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with invalid keyword should return 0 results")
    