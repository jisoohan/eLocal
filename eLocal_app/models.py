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
        return list(Item.objects.filter(name__icontains=name))
    
    # Associates this item with a corresponding store and price
    def addToStore(self, storeId, price):
        try:
            store = Store.objects.get(id=storeId)
            inv = Inventory(store=store, item=self, price=Decimal(price))
            return inv
        except Store.DoesNotExist as e:
            raise e
    

class Store(models.Model):
    name      = models.CharField(max_length=128)
    address   = models.CharField(max_length=256)
    latitude  = models.FloatField()
    longitude = models.FloatField()
    # Hours can be accessed using <store>.openhours_set
    items     = models.ManyToManyField(Item, through='Inventory')
    
    @staticmethod
    def addStore(name, address, latitude, longitude):
        # TODO: Validate fields
        store = Store(name=name, address=address, latitude=latitude, longitude=longitude)
        store.save()
        return store
    
    # Get a list of stores whose names match the query string
    @staticmethod
    def getStores(name):
        return list(Store.objects.filter(name__icontains=name))
    
    def setOpenHours(self, dayOfWeek, startTime, endTime, isOpen):
        # TODO: Validate fields
        if startTime > endTime:
            raise ValidationError("Closing hour must be after opening hour")
        days = self.openhours_set.all()
        for day in days:
            if day.weekday == dayOfWeek:
                day.from_hour = startTime
                day.to_hour = endTime
                day.is_open = isOpen
                day.save()
                return
        new_day = OpenHours(store=self,
                            weekday=dayOfWeek,
                            is_open=isOpen,
                            from_hour=startTime,
                            to_hour=endTime)
        new_day.save()
    
    # Associates this store with a corresponding item and price
    def addItem(self, itemId, price):
        try:
            item = Item.objects.get(id=itemId)
            inv = Inventory(store=self, item=item, price=Decimal(price))
            return inv
        except Item.DoesNotExist as e:
            raise e
    

# Adapted from https://stackoverflow.com/questions/8128143/any-existing-solution-to-implement-opening-hours-in-django
class OpenHours(models.Model):
    # Each OpenHours object belongs to one store, but each store has multiple OpenHours
    store     = models.ForeignKey(Store)
    weekday   = models.IntegerField(choices=WEEKDAYS)
    is_open   = models.BooleanField()
    from_hour = models.TimeField()
    to_hour   = models.TimeField()


# Tracks item-store-price associations
class Inventory(models.Model):
    store = models.ForeignKey(Store)
    item  = models.ForeignKey(Item)
    # Using DecimalField instead of FloatField here to enforce precision of prices (i.e. $123.45)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    
    # Get a list of items that the specified store has
    @staticmethod
    def getItemsForStore(storeId):
        try:
            store = Store.objects.get(id=storeId)
            return store.items.all()
        except Store.DoesNotExist as e:
            raise e
    
    # Get a list of stores that have the specified item
    @staticmethod
    def getStoresForItem(itemId):
        try:
            item = Item.objects.get(id=itemId)
            return item.store_set.all()
        except Item.DoesNotExist as e:
            raise e

