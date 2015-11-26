from django.test import TestCase, RequestFactory
from eLocal_app.models import *
from eLocal_app.views import *
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
# Create your tests here.

class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.uvs = UserViewSet()
        self.svs = StoreViewSet()
        
        user_data = {"username":"testuser1", "password":"password1", "is_staff":True}
        user_req = self.factory.post("/auth/register/", data=user_data)
        register(user_req)
        self.user = User.objects.get(username="testuser1")
        
        store_data = {"st_number":"1885", "st_name":"University Avenue", "city":"Berkeley", "state":"CA",
                          "zipcode":94709, "country":"US", "lat":37.871799, "lng":-122.273206, "store_name":"Trader Joe's"}
        store_req = self.factory.post("/stores/create_store/", data=store_data)
        store_req.data = store_data
        self.uvs.create_store(store_req, self.user.id)
        self.store = Store.objects.get(address__lat=37.871799, address__lng=-122.273206)
        
        product_data = {"product_name":"Cookie butter", "description":"Cookiez!!!", "price":3.99}
        product_req = self.factory.post("/stores/add_product", data=product_data)
        product_req.data = product_data
        self.svs.add_product(product_req, self.store.id)
        self.product = Product.objects.get(name="Cookie butter", description="Cookiez!!!")
    
    def tearDown(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Store.objects.all().delete()
        Product.objects.all().delete()
        Address.objects.all().delete()
    
    def testRegisterUser(self):
        good_req = self.factory.post("/auth/register/", data={"username":"testuser2", "password":"password1", "is_staff":False})
        good_resp = register(good_req)
        self.assertEquals(200, good_resp.status_code, "Registering a valid user should return status 200")
        
        bad_req = self.factory.post("/auth/register/", data={"username":"testuser1", "password":"other-password", "is_staff":True})
        bad_resp = register(bad_req)
        self.assertEquals(400, bad_resp.status_code, "Registering an existing user should return status 400")
    
    def testCreateStore(self):
        good_data = {"st_number":"1886", "st_name":"University Avenue", "city":"Berkeley", "state":"CA", "has_card":True,
                          "zipcode":94709, "country":"US", "lat":37.871779, "lng":-122.273226, "store_name":"Trader Joe's 2"}
        good_req = self.factory.post("/stores/create_store/", data=good_data)
        good_req.data = good_data
        good_resp = self.uvs.create_store(good_req, self.user.id)
        self.assertEquals(200, good_resp.status_code, "Creating a valid store should return status 200")
        
        dup_data = {"st_number":"1885", "st_name":"University Avenue", "city":"Berkeley", "state":"CA", "has_card":True,
                          "zipcode":94709, "country":"US", "lat":37.871799, "lng":-122.273206, "store_name":"Trader Joe's"}
        dup_req = self.factory.post("/stores/create_store/", data=dup_data)
        dup_req.data = dup_data
        dup_resp = self.uvs.create_store(dup_req, self.user.id)
        self.assertEquals(400, dup_resp.status_code, "Creating a duplicate store should return status 400")
    
    def testStoresInZipcode(self):
        good_data = {"lat":37.871729, "lng":-122.273323, "radius":5}
        good_req = self.factory.post("/stores/stores_in_zipcode", data=good_data)
        good_req.data = good_data
        good_resp = self.svs.stores_in_zipcode(good_req)
        self.assertEquals(200, good_resp.status_code, "Valid store search should return status 200")
        self.assertEquals(1, len(good_resp.data), "Valid store search should return stores in range")
        
        bad_data = {"lat":37.0, "lng":-122.9, "radius":5}
        bad_req = self.factory.post("/stores/stores_in_zipcode", data=bad_data)
        bad_req.data = bad_data
        bad_resp = self.svs.stores_in_zipcode(bad_req)
        self.assertEquals(200, bad_resp.status_code, "Out-of-range store search should return status 200")
        self.assertEquals(0, len(bad_resp.data), "Out-of-range store search should return zero stores")
        
    def testProductsInZipcode(self):
        good_data = {"lat":37.871729, "lng":-122.273323, "radius":5}
        good_req = self.factory.post("/stores/products_in_zipcode", data=good_data)
        good_req.data = good_data
        good_resp = self.svs.products_in_zipcode(good_req)
        self.assertEquals(200, good_resp.status_code, "Valid store search should return status 200")
        self.assertEquals(1, len(good_resp.data), "Valid store search should return stores in range")
        
        bad_data = {"lat":37.0, "lng":-122.9, "radius":5}
        bad_req = self.factory.post("/stores/stores_in_zipcode", data=bad_data)
        bad_req.data = bad_data
        bad_resp = self.svs.products_in_zipcode(bad_req)
        self.assertEquals(200, bad_resp.status_code, "Out-of-range store search should return status 200")
        self.assertEquals(0, len(bad_resp.data), "Out-of-range store search should return zero stores")
    
    def testLogin(self):
        good_data = {"username":"testuser1", "password":"password1"}
        good_req = self.factory.post("/auth/login/", data=good_data)
        good_resp = login(good_req)
        self.assertEquals(200, good_resp.status_code, "Valid user logging in should return status 200")
        
        bad_data1 = {"username":"testuser1", "password":"badpassword"}
        bad_req1 = self.factory.post("/auth/login/", data=bad_data1)
        bad_resp1 = login(bad_req1)
        self.assertEquals(400, bad_resp1.status_code, "User logging in with bad password should return status 400")
        
        bad_data2 = {"username":"baduser", "password":"password1"}
        bad_req2 = self.factory.post("/auth/login/", data=bad_data2)
        bad_resp2 = login(bad_req2)
        self.assertEquals(400, bad_resp2.status_code, "Logging in with invalid username should return status 400")
        
        bad_data3 = {"username":"baduser", "password":"password1"}
        bad_req3 = self.factory.get("/auth/login/", data=bad_data3)
        bad_resp3 = login(bad_req3)
        self.assertEquals(405, bad_resp3.status_code, "GET request to login URL should return status 405")
    
    def testMerchantStoreInfo(self):
        good_req = self.factory.get("/stores/merchant_store_info")
        good_req.user = self.user
        good_resp = self.svs.merchant_store_info(good_req, pk=good_req.user.id)
        self.assertEquals(200, good_resp.status_code, "Valid merchant getting store info should return status 200")
        
        bad_req = self.factory.get("/stores/merchant_store_info")
        bad_req.user = self.user
        bad_resp = self.svs.merchant_store_info(bad_req, pk=-1)
        self.assertEquals(400, bad_resp.status_code, "Merchant getting info for other user's store should return status 400")
    
    
    def testEditProduct(self):
        good_data1 = {"price":3.49}
        good_req1 = self.factory.post("/stores/edit_product", data=good_data1)
        good_req1.data = good_data1
        good_resp1 = self.svs.edit_product(good_req1, pk=self.product.id)
        self.assertEquals(200, good_resp1.status_code, "Updating price of valid item should return status 200")
        
        good_data2 = {"product_name":"NEW cookie butter", "description":"It's new!", "price":3.49}
        good_req2 = self.factory.post("/stores/edit_product", data=good_data2)
        good_req2.data = good_data2
        good_resp2 = self.svs.edit_product(good_req2, pk=self.product.id)
        self.assertEquals(200, good_resp2.status_code, "Updating name, description, and price of valid item should return status 200")
        
        bad_data = {"price":3.49}
        bad_req = self.factory.post("/stores/edit_product", data=bad_data)
        bad_req.data = bad_data
        bad_resp = self.svs.edit_product(bad_req, pk=-1)
        self.assertEquals(400, bad_resp.status_code, "Updating price of invalid item should return status 400")