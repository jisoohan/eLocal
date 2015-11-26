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
        self.user_id = User.objects.get(username="testuser1").id
        
        store_data = {"st_number":"1885", "st_name":"University Avenue", "city":"Berkeley", "state":"CA",
                          "zipcode":94709, "country":"US", "lat":37.871799, "lng":-122.273206, "store_name":"Trader Joe's"}
        store_req = self.factory.post("/stores/create_store/", data=store_data)
        store_req.data = store_data
        self.uvs.create_store(store_req, self.user_id)
        self.store_id = Store.objects.get(address__lat=37.871799, address__lng=-122.273206).id
        
        product_data = {"product_name":"Cookie butter", "description":"Cookiez!!!", "price":3.99}
        product_req = self.factory.post("/stores/add_product", data=product_data)
        product_req.data = product_data
        self.svs.add_product(product_req, self.store_id)
    
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
        good_resp = self.uvs.create_store(good_req, self.user_id)
        self.assertEquals(200, good_resp.status_code, "Creating a valid store should return status 200")
        
        dup_data = {"st_number":"1885", "st_name":"University Avenue", "city":"Berkeley", "state":"CA", "has_card":True,
                          "zipcode":94709, "country":"US", "lat":37.871799, "lng":-122.273206, "store_name":"Trader Joe's"}
        dup_req = self.factory.post("/stores/create_store/", data=dup_data)
        dup_req.data = dup_data
        dup_resp = self.uvs.create_store(dup_req, self.user_id)
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
        