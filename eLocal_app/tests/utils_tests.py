from django.test import TestCase
from eLocal_app.models import *
from eLocal_app.views import *
#from eLocal_app.utils import ElocalUtils
#from django.forms.models import model_to_dict
from operator import itemgetter
import googlemaps
import unittest
#import mox

class UtilTest(TestCase):

	def setUp(self):
		Address.objects.all().delete()
		Product.objects.all().delete()
		Store.objects.all().delete()

	def tearDown(self):
		Address.objects.all().delete()
		Product.objects.all().delete()
		Store.objects.all().delete()

	def testJsonResponse(self):
		fakeResponseDict = {'username': 'alexa', 'token': '7c9e2a54c299a2920932b34e3bfee461eeae0648', 'userId': 1}
		response = json_response(fakeResponseDict, 200)
		self.assertEquals(200, response.status_code, "Issue with json_response utility in utils.py")
		

	
