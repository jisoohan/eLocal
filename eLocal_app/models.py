from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from time import time
from decimal import *

# Adapted from https://stackoverflow.com/questions/8128143/any-existing-solution-to-implement-opening-hours-in-django
WEEKDAYS = (
  (0, "Sunday"),
  (1, "Monday"),
  (2, "Tuesday"),
  (3, "Wednesday"),
  (4, "Thursday"),
  (5, "Friday"),
  (6, "Saturday"),
)

STATES = (
    (0, "AL"),
    (1, "AK"),
    (2, "AZ"),
    (3, "AR"),
    (4, "CA"),
    (5, "CO"),
    (6, "CT"),
    (7, "DE"),
    (8, "FL"),
    (9, "GA"),
    (10, "HI"),
    (11, "ID"),
    (12, "IL"),
    (13, "IN"),
    (14, "IA"),
    (15, "KS"),
    (16, "KY"),
    (17, "LA"),
    (18, "ME"),
    (19, "MD"),
    (20, "MA"),
    (21, "MI"),
    (22, "MN"),
    (23, "MS"),
    (24, "MO"),
    (25, "MT"),
    (26, "NE"),
    (27, "NV"),
    (28, "NH"),
    (29, "NJ"),
    (30, "NM"),
    (31, "NY"),
    (32, "NC"),
    (33, "ND"),
    (34, "OH"),
    (35, "OK"),
    (36, "OR"),
    (37, "PA"),
    (38, "RI"),
    (39, "SC"),
    (40, "SD"),
    (41, "TN"),
    (42, "TX"),
    (43, "UT"),
    (44, "VT"),
    (45, "VA"),
    (46, "WA"),
    (47, "WV"),
    (48, "WI"),
    (49, "WY"),
    (50, "DC"),
)


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    # Stores can be accessed using <item>.store_set

    @staticmethod
    def create(name, description):
        # Validate field
        errors = []
        if not validateStringLen(name, 1, 128):
            errors.append("Item name must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(description, 1, 1024):
            errors.append("Item description must be a non-empty string 1 to 1024 characters long")
        if len(errors) > 0:
            raise ValidationError(errors)

        name = name.strip()
        description = description.strip()
        item = Item(name=name, description=description)
        item.save()
        return item

    # Get a list of items whose names match the query string
    @staticmethod
    def getItems(name):
        # Validate field
        errors = []
        if not validateStringLen(name, 1, 128):
            errors.append("Item name must be a non-empty string 1 to 128 characters long")
        if len(errors) > 0:
            raise ValidationError(errors)

        name = name.strip()
        return list(Item.objects.filter(name__icontains=name))

    # Associates this item with a corresponding store and price
    def addToStore(self, storeId, price):
        # Validate fields
        errors = []
        store = None
        if not validateFloatOpenSet(price, 0, 1e6):
            errors.append("Price must be nonzero and less than $1,000,000")
        try:
            store = Store.objects.get(id=storeId)
        except Store.DoesNotExist:
            errors.append("Invalid item ID")
        if len(errors) > 0:
            raise ValidationError(errors)

        inv = Inventory.create(store, self, price)
        return inv


class Store(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=128)
    has_card = models.BooleanField()
    # Hours can be accessed using <store>.openhours_set
    items = models.ManyToManyField(Item, through='Inventory')

    @staticmethod
    def create(name, address, city, state, zip_code, country, has_card):
        # Validate fields
        errors = []
        if not validateStringLen(name, 1, 128):
            errors.append("Name must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(address, 1, 256):
            errors.append("Address must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(city, 1, 128):
            errors.append("City must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(state, 1, 2):
            errors.append("State must be a non-empty string 2 characters long")
        if not validateStringLen(zip_code, 1, 10):
            errors.append("Zipcode must be a non-empty string 1 to 10 characters long")
        if not validateStringLen(country, 1, 128):
            errors.append("Country must be a non-empty string 1 to 128 characters long")

        if len(errors) > 0:
            raise ValidationError(errors)

        store = Store(name=name, address=address, city=city, state=state, zip_code=zip_code, country=country, has_card=has_card)
        store.save()
        return store

    # Get a list of stores whose names match the query string
    @staticmethod
    def getStores(name):
        # Validate field
        errors = []
        if not validateStringLen(name, 1, 128):
            errors.append("Store name must be a non-empty string 1 to 128 characters long")
        if len(errors) > 0:
            raise ValidationError(errors)

        name = name.strip()
        return list(Store.objects.filter(name__icontains=name))

    def setOpenHours(self, dayOfWeek, startTime, endTime, isOpen=True):
        # Validate fields
        # TODO: use OpenHours's validation
        errors = []
        if not validateWeekday(dayOfWeek):
            errors.append("Day of week must be between 0 and 6 inclusive")
        if not isinstance(startTime, time):
            errors.append("Opening time must be a valid time object")
        if not isinstance(endTime, time):
            errors.append("Closing time must be a valid time object")
        if not isinstance(isOpen, bool):
            errors.append("isOpen flag must be true or false")
        if startTime > endTime and isOpen:
            errors.append("Closing time must be after opening time")
        if len(errors) > 0:
            raise ValidationError(errors)

        days = self.openhours_set.all()
        for day in days:
            if day.weekday == dayOfWeek:
                day.from_hour = startTime
                day.to_hour = endTime
                day.is_open = isOpen
                day.save()
                return day
        new_day = OpenHours.create(self, dayOfWeek, startTime, endTime, isOpen)
        return new_day

    # Associates this store with a corresponding item and price
    def addItem(self, itemId, price):
        # Validate fields
        errors = []
        item = None
        if not validateFloatOpenSet(price, 0, 1e6):
            errors.append("Price must be nonzero and less than $1,000,000")
        try:
            item = Item.objects.get(id=itemId)
        except Item.DoesNotExist:
            errors.append("Invalid item ID")
        if len(errors) > 0:
            raise ValidationError(errors)

        inv = Inventory.create(self, item, price)
        return inv


# Adapted from https://stackoverflow.com/questions/8128143/any-existing-solution-to-implement-opening-hours-in-django
class OpenHours(models.Model):
    # Each OpenHours object belongs to one store, but each store has multiple OpenHours
    store     = models.ForeignKey(Store)
    weekday   = models.IntegerField(choices=WEEKDAYS)
    is_open   = models.BooleanField()
    from_hour = models.TimeField()
    to_hour   = models.TimeField()

    @staticmethod
    def create(store, weekday, from_hour, to_hour, is_open):
        # Validate fields
        errors = []
        if not isinstance(store, Store):
            errors.append("Invalid store object")
        if not validateWeekday(weekday):
            errors.append("Day of week must be between 0 and 6 inclusive")
        if not isinstance(from_hour, time):
            errors.append("Opening time must be a valid time object")
        if not isinstance(to_hour, time):
            errors.append("Closing time must be a valid time object")
        if not isinstance(is_open, bool):
            errors.append("isOpen flag must be true or false")
        if from_hour >= to_hour and is_open:
            errors.append("Closing time must be after opening time")
        if len(errors) > 0:
            raise ValidationError(errors)

        new_day = OpenHours(store=store,
                            weekday=weekday,
                            is_open=is_open,
                            from_hour=from_hour,
                            to_hour=to_hour)
        new_day.save()
        return new_day


# Tracks item-store-price associations
class Inventory(models.Model):
    store = models.ForeignKey(Store)
    item  = models.ForeignKey(Item)
    # Using DecimalField instead of FloatField here to enforce precision of prices (i.e. $123.45)
    price = models.DecimalField(decimal_places=2, max_digits=8)

    @staticmethod
    def create(store, item, price):
        errors = []
        if not isinstance(store, Store):
            errors.append("Invalid store object")
        if not isinstance(item, Item):
            errors.append("Invalid item object")
        if not validateFloatOpenSet(price, 0, 1e6):
            errors.append("Price must be nonzero and less than $1,000,000")
        if len(errors) > 0:
            raise ValidationError(errors)

        inv = Inventory(store=store, item=item, price=price)
        inv.save()
        return inv

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

    @staticmethod
    def getPrice(storeId, itemId):
        try:
            return float(Inventory.objects.get(store__id__exact=storeId, item__id__exact=itemId).price)
        except Inventory.DoesNotExist as e:
            raise e


def validateStringLen(string, min_len, max_len):
    if not isinstance(string, str):
        return False
    if not (min_len <= len(string) <= max_len):
        return False
    return True

def validateFloatOpenSet(num, minimum, maximum):
    if not isinstance(num, float) and not isinstance(num, int):
        return False
    if num < minimum or num > maximum:
        return False
    return True

def validateWeekday(day):
    if not isinstance(day, int):
        return False
    for weekday, _ in WEEKDAYS:
        if day == weekday:
            return True
    return False

