from django.test import TestCase
from eLocal_app.models import Item, Store, Inventory, OpenHour
from django.core.exceptions import ValidationError
from datetime import time as TimeOfDay
from eLocal_app import utils, views
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
        with self.assertRaises(Item.DoesNotExist, msg="Getting stores for invalid item ID should fail"):
            result = Inventory.getStoresForItem(-1)
     
    def testInvalidStoreId(self):
        with self.assertRaises(Store.DoesNotExist, msg="Getting items for invalid store ID should fail"):
            result = Inventory.getItemsForStore(-1)
    
    def testCreateInvalidItem(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        with self.assertRaises(ValueError, msg="Creating inventory with invalid store should fail"):
            Inventory.create(store1, None, 3.0)
    
    def testCreateInvalidPrice(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        item1 = Item.create("Test item 1", "Test description")
        for arg, msg in ((None, "null"),
                              (0.0, "zero"),
                              (1000000.0, "overly large")):
            with self.assertRaises(ValidationError, msg="Creating inventory with {0} price should fail".format(msg)):
                Inventory.create(store1, item1, arg)

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
        for arg, msg in ((None, "null"),
                              ("", "empty"),
                              ("A"*129, "overly long"),
                              (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Item search with {0} keyword should fail".format(msg)):
                Item.getItems(arg)
        
    def testCreateInvalidItem(self):
        i = 0
        for min_len, max_len, field in ((1, 128, "name"),
                                        (1, 1024, "description")):
            for arg, msg in ((None, "null"),
                              ("", "empty"),
                              ("A"*max(min_len-1, 0), "overly short"),
                              ("A"*(max_len+1), "overly long"),
                              (1, "non-string")):
                i += 1
                with self.assertRaises(ValidationError, msg="Creating store with {0} {1} should fail".format(msg, field)):
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
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        self.assertEqual("Test store 1", store1.name, "Store name is not correctly stored")
        self.assertEqual("Test address", store1.address, "Store address is not correctly stored")
        self.assertEqual("Test city", store1.city, "Store city is not correctly stored")
        self.assertEqual("CA", store1.state, "Store state is not correctly stored")
        self.assertEqual("12345", store1.zip_code, "Store ZIP code is not correctly stored")
        self.assertEqual("US", store1.country, "Store country is not correctly stored")
        self.assertEqual(False, store1.has_card, "Store has_card is not correctly stored")
        self.assertEqual(1.0, store1.latitude, "Store latitude is not correctly stored")
        self.assertEqual(-2.0, store1.longitude, "Store longitude is not correctly stored")
    
    def testSearchStore(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        store2 = Store.create("Another shop", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        store3 = Store.create("Third stOre", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        search_1 = Store.getStores("Test store 1")
        self.assertEqual(len(search_1), 1, "Store search with full string should return one store")
        self.assertEqual(store1.id, search_1[0].id, "Store search returned irrelevant store")
        search_2 = Store.getStores("sTorE 1")
        self.assertEqual(len(search_2), 1, "Store search should be case-insensitive and should return one store")
        self.assertEqual(store1.id, search_2[0].id, "Store search returned irrelevant store")
        result = Store.getStores('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with invalid keyword should return 0 results")
    
    
    def testSearchInvalidStore(self):
        for arg, msg in ((None, "null"),
                              ("A"*129, "overly long"),
                              (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Searching for {0} store name should fail"):
                Store.getStores(arg)
    
    def testCreateInvalidStoreStrings(self):
        i = 0
        for min_len, max_len, field in ((1, 128, "name"),
                                        (1, 256, "address"),
                                        (1, 128, "city"),
                                        (2, 2, "state"),
                                        (5, 10, "ZIP code"),
                                        (1, 128, "country")):
            for arg, msg in ((None, "null"),
                              ("", "empty"),
                              ("A"*max(min_len-1, 0), "overly short"),
                              ("A"*(max_len+1), "overly long"),
                              (1, "non-string")):
                i += 1
                store_name = "Test store " + str(i)
                with self.assertRaises(ValidationError, msg="Creating store with {0} {1} should fail".format(msg, field)):
                    if field == "name":
                        Store.create(arg, "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
                    elif field == "address":
                        Store.create(store_name, arg, "Test city", "CA", "12345", "US", False, 1.0, -2.0)
                    elif field == "city":
                        Store.create(store_name, "Test address", arg, "CA", "12345", "US", False, 1.0, -2.0)
                    elif field == "state":
                        Store.create(store_name, "Test address", "Test city", arg, "12345", "US", False, 1.0, -2.0)
                    elif field == "ZIP code":
                        Store.create(store_name, "Test address", "Test city", "CA", arg, "US", False, 1.0, -2.0)
                    elif field == "country":
                        Store.create(store_name, "Test address", "Test city", "CA", "12345", arg, False, 1.0, -2.0)

    def testCreateInvalidStoreHasCard(self):
        for arg, msg in ((None, "null"),
                              (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Creating store with {0} has-card status should fail".format(msg)):
                Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", arg, 1.0, -2.0)
    
    def testCreateInvalidStoreCoords(self):
        for arg, msg in ((None, "null"),
                             (90.1, "too-large"),
                             (-90.1, "too-small"),
                             ("1.2", "non-float")):
            with self.assertRaises(ValidationError, msg="Creating store with {0} latitude should fail".format(msg)):
                Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", False, arg, -2.0)
        for arg, msg in ((None, "null"),
                             (180.1, "too-large"),
                             (-180.1, "too-small"),
                             ("1.2", "non-float")):
            with self.assertRaises(ValidationError, msg="Creating store with {0} latitude should fail".format(msg)):
                Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", False, 1.0, arg)
    
    def testAddInvalidAddItem(self):
        store1 = Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        with self.assertRaises(ValidationError, msg="Adding invalid item to store should fail"):
            store1.addItem(-1, 3.0)
    
    
class OpenHourTest(TestCase):
    def setUp(self):
        OpenHour.objects.all().delete()
        Store.objects.all().delete()
    
    def tearDown(self):
        OpenHour.objects.all().delete()
        Store.objects.all().delete()
    
    def testCreateOpenHour(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        hours = OpenHour.create(store1, "Wednesday", TimeOfDay(9), TimeOfDay(21), False)
        hours_set = store1.openhour_set.all()
        self.assertEquals(1, len(hours_set), "Wrong number of open hours was saved")
        self.assertEquals(hours, hours_set[0], "Open hours were not properly saved")
    
    
    def testInvalidOpenHourDay(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        for arg, msg in ((None, "null"),
                             ("A"*10, "too-large"),
                             ("", "too-small"),
                             (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Creating open hours with {0} day should fail".format(msg)):
                OpenHour.create(store1, arg, TimeOfDay(9), TimeOfDay(21), False)

    def testInvalidOpenHourTimes(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        for arg1, arg2, msg in ((None, None, "null times"),
                             (TimeOfDay(20), TimeOfDay(19), "end before start")):
            with self.assertRaises(ValidationError, msg="Creating open hours with {0} should fail".format(msg)):
                OpenHour.create(store1, "Tuesday", arg1, arg2, False)

    def testInvalidOpenHourStore(self):
        for arg, msg in ((None, "null"),
                             (1, "wrong type for")):
            with self.assertRaises(ValueError, msg="Creating open hours with {0} store should fail".format(msg)):
                OpenHour.create(arg, "Wednesday", TimeOfDay(9), TimeOfDay(21), False)
    
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
        store = Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        inventory = store.addItem(item.id, 12345.67)
        self.assertEqual(1, len(Inventory.getStoresForItem(item.id)), "Item should remember the store that it is added to")
        self.assertEqual(1, len(Inventory.getItemsForStore(store.id)), "Store should remember the item that it has")
        self.assertEqual(12345.67, Inventory.getPrice(store.id, item.id), "Inventory should remember a store's price for an item")