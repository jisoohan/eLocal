from django.test import TestCase, RequestFactory
from eLocal_app.models import *
from eLocal_app.views import *
from eLocal_app.forms import *
from django.core.exceptions import ValidationError
# Create your tests here.

class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def tearDown(self):
        pass
    
    def testHomePageGet(self):
        request = self.factory.post("/")
        request.session = {}
        response = homePage(request)
        self.assertEquals(200, response.status_code, "Sending GET to homepage should return OK")
    
    def testHomePagePost(self):
        request = self.factory.post("/")
        request.session = {}
        request.POST = {"radius":5, "zip_code":"94720"}
        response = homePage(request)
        self.assertEquals(302, response.status_code, "Sending valid POST to homepage should return redirect")
    
    def testAddStore(self):
        request = self.factory.post("/")
        request.session = {"coordinates":[[37, -121]], "radius":5}
        request.POST = {"store_name":"Test store", "street_number":"12345", "street_address":"Test street",
                        "city":"Berkeley", "state":"CA", "zip_code":"94720", "country":"US", "has_card":False}
        response = addStore(request)
        self.assertEquals(302, response.status_code, "Sending POST to add store with valid form should return redirect")
        self.assertEquals("/stores", response.url, "Sending valid POST to add store should redirect to /stores")
    