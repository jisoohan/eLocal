from django.test import TestCase
from eLocal_app.models import Address, Store, Product
from django.core.exceptions import ValidationError
from datetime import time as TimeOfDay
# Create your tests here.

class InventoryTest(TestCase):
    def setUp(self):
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Store.objects.all().delete()
    
    def tearDown(self):
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Store.objects.all().delete()
    
    def testSearchInvalidProductId(self):
        with self.assertRaises(Product.DoesNotExist, msg="Getting stores for invalid Product ID should fail"):
            result = Inventory.getStoresForProduct(-1)
     
    def testSearchInvalidStoreId(self):
        with self.assertRaises(Store.DoesNotExist, msg="Getting Products for invalid store ID should fail"):
            result = Inventory.getProductsForStore(-1)
    
    def testCreateInvalidProduct(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        with self.assertRaises(ValueError, msg="Creating inventory with invalid store should fail"):
            Inventory.create(store1, None, 3.0)
    
    def testCreateInvalidPrice(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        Product1 = Product.create("Test Product 1", "Test description")
        for arg, msg in ((None, "null"),
                              (0.0, "zero"),
                              (1000000.0, "overly large")):
            with self.assertRaises(ValidationError, msg="Creating inventory with {0} price should fail".format(msg)):
                Inventory.create(store1, Product1, arg)
    
    def testHasDuplicateProduct(self):
        Product1 = Product.create("Test Product 1", "Test description")
        Product2 = Product.create("Another thing", "Test description")
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        Inventory.create(store1, Product1, 3.0)
        self.assertTrue(Inventory.hasDuplicateProduct(Product1.name, store1.id), "Inventory does not properly detect duplicate Products")
        self.assertFalse(Inventory.hasDuplicateProduct(Product2.name, store1.id), "Inventory falsely detects duplicate Products")
        
    
class ProductTest(TestCase):
    def setUp(self):
        Product.objects.all().delete()
    
    def tearDown(self):
        Product.objects.all().delete()
    
    def testSearchProduct(self):
        Product1 = Product.create("Test Product 1", "Test description")
        Product2 = Product.create("Another thing", "Test description")
        Product3 = Product.create("Third Product", "Test description")
        search_1 = Product.getProducts("Test Product 1")
        self.assertEqual(len(search_1), 1, "Product search with full string should return one Product")
        self.assertEqual(Product1.id, search_1[0].id, "Product search returned irrelevant Product")
        search_2 = Product.getProducts("Product 1")
        self.assertEqual(len(search_2), 1, "Product search should be case-insensitive and should return one Product")
        self.assertEqual(Product1.id, search_2[0].id, "Product search returned irrelevant Product")
        result = Product.getProducts('HUi887zu8HDzdKNNarDXujvvkzE')
        self.assertEqual(0, len(result), "Store queries with non-matching keyword should return 0 results")
    
    def testSearchInvalidProduct(self):
        for arg, msg in ((None, "null"),
                              ("", "empty"),
                              ("A"*129, "overly long"),
                              (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Product search with {0} keyword should fail".format(msg)):
                Product.getProducts(arg)
    
    def testCreateProduct(self):
        Product1 = Product.create("Test Product 1", "Test description")
        self.assertEqual("Test Product 1", Product1.name, "Product name is not correctly stored")
    
    def testCreateInvalidProduct(self):
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
                        Product.create(arg, "Test description")
                    elif field == "description":
                        Product.create("Test Product " + str(i), arg)
    
    def testAddInvalidStore(self):
        Product = Product.create("Test Product", "Test description")
        with self.assertRaises(ValidationError, msg="Adding Product to invalid store should fail"):
            Product.addToStore(-1, 3.0)
    
    def testAddToStore(self):
        Product = Product.create("Test Product", "Test description")
        store = Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        Product.addToStore(store.id, 3.0)
        self.assertEquals(1, len(Product.store_set.all()), "Product does not properly record its stores")
        
    
class StoreTest(TestCase):
    def setUp(self):
        Store.objects.all().delete()
    
    def tearDown(self):
        Store.objects.all().delete()
    
    def testAddInvalidProduct(self):
        store1 = Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        with self.assertRaises(ValidationError, msg="Adding invalid Product to store should fail"):
            store1.addProduct(-1, 3.0)
    
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
    
    
    def testCreateInvalidOHDay(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        for arg, msg in ((None, "null"),
                             ("A"*10, "too-large"),
                             ("", "too-small"),
                             (1, "non-string")):
            with self.assertRaises(ValidationError, msg="Creating open hours with {0} day should fail".format(msg)):
                OpenHour.create(store1, arg, TimeOfDay(9), TimeOfDay(21), False)

    
    def testCreateInvalidOHStore(self):
        for arg, msg in ((None, "null"),
                             (1, "wrong type for")):
            with self.assertRaises(ValueError, msg="Creating open hours with {0} store should fail".format(msg)):
                OpenHour.create(arg, "Wednesday", TimeOfDay(9), TimeOfDay(21), False)
    

    def testCreateInvalidOHTimes(self):
        store1 = Store.create("Test store 1", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        for arg1, arg2, msg in ((None, None, "null times"),
                                (1, TimeOfDay(20), "bad type for start"),
                                (TimeOfDay(20), TimeOfDay(19), "end before start")):
            with self.assertRaises(ValidationError, msg="Creating open hours with {0} should fail".format(msg)):
                OpenHour.create(store1, "Tuesday", arg1, arg2, False)

class ModelFunctionalTest(TestCase):
    def setUp(self):
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Store.objects.all().delete()
    
    def tearDown(self):
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Store.objects.all().delete()

    def testAddInventory(self):
        Product = Product.create("Test Product", "Test description")
        store = Store.create("Test store", "Test address", "Test city", "CA", "12345", "US", False, 1.0, -2.0)
        inventory = store.addProduct(Product.id, 12345.67)
        self.assertEqual(1, len(Inventory.getStoresForProduct(Product.id)), "Product should remember the store that it is added to")
        self.assertEqual(1, len(Inventory.getProductsForStore(store.id)), "Store should remember the Product that it has")
        self.assertEqual(12345.67, Inventory.getPrice(store.id, Product.id), "Inventory should remember a store's price for an Product")