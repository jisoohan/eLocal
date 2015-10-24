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
        item1 = Item.create("Test item 1")
        self.assertEqual("Test item 1", item1.name, "Item name is not correctly stored")
    
    def testSearchItem(self):
        item1 = Item.create("Test item 1")
        item2 = Item.create("Another thing")
        item3 = Item.create("Third itEm")
        search_1 = Item.getItems("Test item 1")
        self.assertEqual(len(search_1), 1, "Item search with full string should return one item")
        self.assertEqual(item1.id, search_1[0].id, "Item search returned irrelevant item")
        search_2 = Item.getItems("iTeM 1")
        self.assertEqual(len(search_2), 1, "Item search should be case-insensitive and should return one item")
        self.assertEqual(item1.id, search_2[0].id, "Item search returned irrelevant item")
        result = Item.getItems('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with non-matching keyword should return 0 results")
    
    def testSearchInvalidItem(self):
        with self.assertRaises(ValidationError, msg="Item search with null keyword should raise exception"):
            Item.getItems(None)
        with self.assertRaises(ValidationError, msg="Item search with empty keyword should raise exception"):
            Item.getItems("")
        with self.assertRaises(ValidationError, msg="Item search with overly long keyword should raise exception"):
            Item.getItems("A"*129)
        with self.assertRaises(ValidationError, msg="Item search with non-string argument should raise exception"):
            Item.getItems(1)
        
    def testCreateInvalidItem(self):
        with self.assertRaises(ValidationError, msg="Creating item with null name should raise exception"):
            Item.create(None)
        with self.assertRaises(ValidationError, msg="Creating item with empty name should raise exception"):
            Item.create("")
        with self.assertRaises(ValidationError, msg="Creating item with overly long name should raise exception"):
            Item.create("A"*129)
        with self.assertRaises(ValidationError, msg="Creating item with non-string name should raise exception"):
            Item.create(1)


class StoreTest(TestCase):
    def setUp(self):
        Store.objects.all().delete()
    
    def tearDown(self):
        Store.objects.all().delete()
    
    def testCreateStore(self):
        store1 = Store.create("Test store 1", "Fake address", 2.7182818, -3.1415926)
        self.assertEqual("Test store 1", store1.name, "Store name is not correctly stored")
        self.assertEqual("Fake address", store1.address, "Store address is not correctly stored")
        self.assertEqual(2.7182818, store1.latitude, "Store latitude are not correctly stored")
        self.assertEqual(-3.1415926, store1.longitude, "Store longitude is not correctly stored")
    
    def testSearchStore(self):
        store1 = Store.create("Test store 1", "Fake address", 2.7182818, -3.1415926)
        store2 = Store.create("Another shop", "Fake address", 2.7182818, -3.1415926)
        store3 = Store.create("Third stOre", "Fake address", 2.7182818, -3.1415926)
        search_1 = Store.getStores("Test store 1")
        self.assertEqual(len(search_1), 1, "Store search with full string should return one store")
        self.assertEqual(store1.id, search_1[0].id, "Store search returned irrelevant store")
        search_2 = Store.getStores("sTorE 1")
        self.assertEqual(len(search_2), 1, "Store search should be case-insensitive and should return one store")
        self.assertEqual(store1.id, search_2[0].id, "Store search returned irrelevant store")
        result = Store.getStores('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with invalid keyword should return 0 results")
    
    def testCreateInvalidStoreName(self):
        with self.assertRaises(ValidationError, msg="Creating store with null name should raise exception"):
            Store.create(None, "Test address", 1, -2)
        with self.assertRaises(ValidationError, msg="Creating store with empty name should raise exception"):
            Store.create("", "Test address", 1, -2)
        with self.assertRaises(ValidationError, msg="Creating store with overly long name should raise exception"):
            Store.create("A"*129, "Test address", 1, -2)
        with self.assertRaises(ValidationError, msg="Creating store with non-string name should raise exception"):
            Store.create(1, "Test address", 1, -2)
        
    def testCreateInvalidStoreAddress(self):
        with self.assertRaises(ValidationError, msg="Creating store with null address should raise exception"):
            Store.create("Test store", None, 1, -2)
        with self.assertRaises(ValidationError, msg="Creating store with empty address should raise exception"):
            Store.create("Test store", "", 1, -2)
        with self.assertRaises(ValidationError, msg="Creating store with overly long address should raise exception"):
            Store.create("Test store", "A"*257, 1, -2)
        with self.assertRaises(ValidationError, msg="Creating store with non-string address should raise exception"):
            Store.create("Test store", 1, 1, -2)
        
    def testCreateInvalidCoordinates(self):
        with self.assertRaises(ValidationError, msg="Creating store with invalid longitude should raise exception"):
            Store.create("Test store", "Test address", 5, -180.2)
        with self.assertRaises(ValidationError, msg="Creating store with invalid latitude should raise exception"):
            Store.create("Test store", "Test address", 90.1, 5)
        with self.assertRaises(ValidationError, msg="Creating store with non-string coordinates should raise exception"):
            Store.create("Test store", "Test address", "5", "3")


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
        item = Item.create("Test item")
        store = Store.create("Test store", "Test address", 2.7182818, -3.1415926)
        inventory = store.addItem(item.id, 12345.67)
        self.assertEqual(1, len(Inventory.getStoresForItem(item.id)), "Item should remember the store that it is added to")
        self.assertEqual(1, len(Inventory.getItemsForStore(store.id)), "Store should remember the item that it has")
        self.assertEqual(12345.67, Inventory.getPrice(store.id, item.id), "Inventory should remember a store's price for an item")