from django.test import TestCase
from eLocal_app.models import Item, Store, Inventory
from django.core.exceptions import ValidationError


# Create your tests here.

class InventoryTest(TestCase):
    def setUp(self):
        Inventory.objects.all().delete()
        Item.objects.all().delete()
        Store.objects.all().delete()
    
    def tearDown(self):
        Inventory.objects.all().delete()
        Item.objects.all().delete()
        Store.objects.all().delete()
    
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
    
    def tearDown(self):
        Item.objects.all().delete()
    
    def testCreateItem(self):
        item1 = Item.create("Test item 1", "Test description")
        self.assertEqual("Test item 1", item1.name, "Item name is not correctly stored")
    
    def testSearchItem(self):
        item1 = Item.create("Test item 1", "Test description")
        item2 = Item.create("Another thing", "Test description")
        item3 = Item.create("Third itEm", "Test description")
        search_1 = Item.getItems("Test item 1")
        self.assertEqual(len(search_1), 1, "Item search with full string should return one item")
        self.assertEqual(item1.id, search_1[0].id, "Item search returned irrelevant item")
        search_2 = Item.getItems("iTeM 1")
        self.assertEqual(len(search_2), 1, "Item search should be case-insensitive and should return one item")
        self.assertEqual(item1.id, search_2[0].id, "Item search returned irrelevant item")
        result = Item.getItems('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with non-matching keyword should return 0 results")
    
    def testSearchInvalidItem(self):
        for arg, message in ((None, "null"),
                              ("", "empty"),
                              ("A"*129, "overly long"),
                              (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Item search with {0} keyword should raise exception".format(message)):
                Item.getItems(arg)
        
    def testCreateInvalidItem(self):
        i = 0
        for min_len, max_len, field in ((1, 128, "name"),
                                        (1, 1024, "description")):
            for arg, message in ((None, "null"),
                              ("", "empty"),
                              ("A"*max(min_len-1, 0), "overly short"),
                              ("A"*(max_len+1), "overly long"),
                              (1, "non-string")):
                i += 1
                with self.assertRaises(ValidationError, msg="Creating store with {0} {1} should raise exception".format(message, field)):
                    if field == "name":
                        Item.create(arg, "Test description")
                    elif field == "description":
                        Item.create("Test item " + str(i), arg)

class StoreTest(TestCase):
    def setUp(self):
        Store.objects.all().delete()
    
    def tearDown(self):
        Store.objects.all().delete()
    
    def testCreateStore(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "Test country", False)
        self.assertEqual("Test store 1", store1.name, "Store name is not correctly stored")
        self.assertEqual("Test address", store1.address, "Store address is not correctly stored")
        self.assertEqual("Test city", store1.city, "Store city is not correctly stored")
        self.assertEqual("CA", store1.state, "Store state is not correctly stored")
        self.assertEqual("12345", store1.zip_code, "Store ZIP code is not correctly stored")
        self.assertEqual("Test country", store1.country, "Store country is not correctly stored")
        self.assertEqual(False, store1.has_card, "Store has_card is not correctly stored")
    
    def testSearchStore(self):
        store1 = Store.create("Test store 1", "Fake address", "Test city", "CA", "12345", "Test country", False)
        store2 = Store.create("Another shop", "Fake address", "Test city", "CA", "12345", "Test country", False)
        store3 = Store.create("Third stOre", "Fake address", "Test city", "CA", "12345", "Test country", False)
        search_1 = Store.getStores("Test store 1")
        self.assertEqual(len(search_1), 1, "Store search with full string should return one store")
        self.assertEqual(store1.id, search_1[0].id, "Store search returned irrelevant store")
        search_2 = Store.getStores("sTorE 1")
        self.assertEqual(len(search_2), 1, "Store search should be case-insensitive and should return one store")
        self.assertEqual(store1.id, search_2[0].id, "Store search returned irrelevant store")
        result = Store.getStores('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with invalid keyword should return 0 results")
    
    def testCreateInvalidStoreStrings(self):
        i = 0
        for min_len, max_len, field in ((1, 128, "name"),
                                        (1, 256, "address"),
                                        (1, 128, "city"),
                                        (2, 2, "state"),
                                        (5, 10, "ZIP code"),
                                        (1, 128, "country")):
            for arg, message in ((None, "null"),
                              ("", "empty"),
                              ("A"*max(min_len-1, 0), "overly short"),
                              ("A"*(max_len+1), "overly long"),
                              (1, "non-string")):
                i += 1
                with self.assertRaises(ValidationError, msg="Creating store with {0} {1} should raise exception".format(message, field)):
                    if field == "name":
                        Store.create(arg, "Test address", "Test city", "CA", "12345", "Test country", False)
                    elif field == "address":
                        Store.create("Test store " + str(i), arg, "Test city", "CA", "12345", "Test country", False)
                    elif field == "city":
                        Store.create("Test store " + str(i), "Test address", arg, "CA", "12345", "Test country", False)
                    elif field == "state":
                        Store.create("Test store " + str(i), "Test address", "Test city", arg, "12345", "Test country", False)
                    elif field == "ZIP code":
                        Store.create("Test store " + str(i), "Test address", "Test city", "CA", arg, "Test country", False)
                    elif field == "country":
                        Store.create("Test store " + str(i), "Test address", "Test city", "CA", "12345", arg, False)

    def testCreateInvalidStoreHasCard(self):
        for arg, message in ((None, "null"),
                              (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Creating store with {0} has-card status should raise exception".format(message)):
                Store.create("Test store", "Test address", "Test city", "CA", "12345", "Test country", arg)
    
class ModelFunctionalTest(TestCase):
    def setUp(self):
        Inventory.objects.all().delete()
        Item.objects.all().delete()
        Store.objects.all().delete()
    
    def tearDown(self):
        Inventory.objects.all().delete()
        Item.objects.all().delete()
        Store.objects.all().delete()

    def testAddInventory(self):
        item = Item.create("Test item", "Test description")
        store = Store.create("Test store", "Test address", "Test city", "CA", "12345", "Test country", False)
        inventory = store.addItem(item.id, 12345.67)
        self.assertEqual(1, len(Inventory.getStoresForItem(item.id)), "Item should remember the store that it is added to")
        self.assertEqual(1, len(Inventory.getItemsForStore(store.id)), "Store should remember the item that it has")
        self.assertEqual(12345.67, Inventory.getPrice(store.id, item.id), "Inventory should remember a store's price for an item")