from django.test import TestCase
from eLocal_app.models import Inventory, Item, Store
from eLocal_app.utils import ElocalUtils
from django.forms.models import model_to_dict
from operator import itemgetter
import googlemaps
import unittest
#import mox

class UtilTest(TestCase):

	def testGeolocateStores(self):
		origin = [(37.86373760000001, -122.2682245)]
		radius = 20
		Store.create("Target", "2187 Shattuck Avenue", "Berkeley", "CA", "94704", "US", False, 37.8696496, -122.2675342)
		Store.create("Target", "789 Mission Street", "San Francisco","CA","94103","US",False,37.7847358,-122.4036914)
		expected = [{'longitude': -122.2675342, 'product_list': [], 'name': 'Target', 'state': 'CA', 'has_card': False, 'latitude': 37.8696496, 'zip_code': '94704', 'address': '2187 Shattuck Avenue', 'country': 'US', 'city': 'Berkeley', 'id': 1}, {'longitude': -122.4036914, 'product_list': [], 'name': 'Target', 'state': 'CA', 'has_card': False, 'latitude': 37.7847358, 'zip_code': '94103', 'address': '789 Mission Street', 'country': 'US', 'city': 'San Francisco', 'id': 2}]
		#print(ElocalUtils.geolocateStores(origin,radius))
		self.assertEquals(expected, ElocalUtils.geolocateStores(origin,radius), "Problem with geolocate stores")
	# def testGetCoorFromZipcode(self):
	# 	zipcode = 94704
	# 	sampleLocation = [{'formatted_address': 'Berkeley, CA 94704, USA',
	# 	 'types': ['postal_code'],
	# 	  'geometry': {'location_type': 'APPROXIMATE',
	# 	   'bounds': {'southwest': {'lat': 37.859769, 'lng': -122.273855},
	# 	    'northeast': {'lat': 37.87412, 'lng': -122.234669}},
	# 	     'viewport': {'southwest': {'lat': 37.859769, 'lng': -122.273855},
	# 	      'northeast': {'lat': 37.87412, 'lng': -122.234669}},
	# 	       'location': {'lat': 37.86373760000001, 'lng': -122.2682245}},
	# 	        'address_components': [{'types': ['postal_code'],
	# 	         'short_name': '94704', 'long_name': '94704'},
	# 	          {'types': ['locality', 'political'],
	# 	           'short_name': 'Berkeley', 'long_name': 'Berkeley'},
	# 	            {'types': ['administrative_area_level_2', 'political'],
	# 	             'short_name': 'Alameda County', 'long_name': 'Alameda County'},
	# 	              {'types': ['administrative_area_level_1', 'political'],
	# 	               'short_name': 'CA','long_name': 'California'},
	# 	                {'types': ['country', 'political'],
	# 	                 'short_name': 'US', 'long_name': 'United States'}],
	# 	                  'place_id': 'ChIJk5trQy58hYARnl9MIbSf6aU'}]
	# 	self.assertEquals(ElocalUtils.getCoorFromZipcode('94704'),[(37.86373760000001, -122.2682245)],"Problem with get coordinates from zipcode")
