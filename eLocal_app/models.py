from django.db import models
from django.core.exceptions import ValidationError
from time import time

# Adapted from https://stackoverflow.com/questions/8128143/any-existing-solution-to-implement-opening-hours-in-django
WEEKDAYS = [
  (0, "Sunday"),
  (1, "Monday"),
  (2, "Tuesday"),
  (3, "Wednesday"),
  (4, "Thursday"),
  (5, "Friday"),
  (6, "Saturday")
]


class Item(models.Model):
    name = models.CharField(max_length=128)
    # Stores can be accessed using <item>.store_set
    
    # Get a list of items whose names match the query string
    @staticmethod
    def getItems(name):
        pass
    
    # Associates this item with a corresponding store and price
    def addToStore(self, name, storeId, price):
        pass
    

class Store(models.Model):
    name      = models.CharField(max_length=128)
    address   = models.CharField(max_length=256)
    latitude  = models.FloatField()
    longitude = models.FloatField()
    # Hours can be accessed using <store>.openhours_set
    items     = models.ManyToManyField(Item, through='Inventory')
    
    @staticmethod
    def addStore(name, address, latitude, longitude, hours):
        pass
    
    # Get a list of stores whose names match the query string
    @staticmethod
    def getStores(name):
        pass
    
    # Associates this store with a corresponding item and price
    def addItem(self, itemId, price):
        pass
    

# Adapted from https://stackoverflow.com/questions/8128143/any-existing-solution-to-implement-opening-hours-in-django
class OpenHours(models.Model):
    # Each OpenHours object belongs to one store, but each store has multiple OpenHours
    store     = models.ForeignKey(Store)
    weekday   = models.IntegerField(choices=WEEKDAYS, unique=True)
    is_open   = models.BooleanField()
    from_hour = models.TimeField()
    to_hour   = models.TimeField()


# Tracks item-store-price associations
class Inventory(models.Model):
    store = models.ForeignKey(Store)
    item = models.ForeignKey(Item)
    # Using DecimalField instead of FloatField here to enforce precision of prices (i.e. $123.45)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    
    # Get a list of stores that carry the specified item
    @staticmethod
    def getItemsForStore(storeId):
        pass
    
    # Get a list of items that the specified store carries
    @staticmethod
    def getStoresForItem(itemId):
        pass

