from django.db import models
from django.core.exceptions import ValidationError
from time import time
from decimal import *

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
        if not validateNumOpenSet(price, 0, 1e6):
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
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    country = models.CharField(max_length=2)
    has_card = models.BooleanField()
    # Hours can be accessed using <store>.openhour_set
    items = models.ManyToManyField(Item, through='Inventory')

    @staticmethod
    def create(name, address, city, state, zip_code, country, has_card):
        # Validate fields
        errors = []
        if not validateStringLen(name, 1, 128):
            errors.append("Name must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(address, 1, 256):
            errors.append("Address must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(city, 1, 60):
            errors.append("City must be a non-empty string 1 to 60 characters long")
        if not validateStringLen(state, 2, 2):
            errors.append("State must be a non-empty string 2 characters long")
        if not validateStringLen(zip_code, 5, 5):
            errors.append("Zipcode must be a non-empty string 5 characters long")
        if not validateStringLen(country, 2, 2):
            errors.append("Country must be a non-empty string 2 characters long")
        if has_card is not True and has_card is not False:
            errors.append("Has_card must be either true or false")
        if Store.hasDuplicate(name, address, city, state, zip_code, country, has_card):
            errors.append("A matching store already exists")
        if len(errors) > 0:
            raise ValidationError(errors)

        store = Store(name=name, address=address, city=city, state=state, zip_code=zip_code, country=country, has_card=has_card)
        store.save()
        return store

    @staticmethod
    def hasDuplicate(name, address, city, state, zip_code, country, has_card):
        return Store.objects.filter(name__iexact=name, address__iexact=address, city__iexact=city, state__iexact=state, zip_code__iexact=zip_code).exists()

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

    # Associates this store with a corresponding item and price
    def addItem(self, itemId, price):
        # Validate fields
        errors = []
        item = None
        if not validateNumOpenSet(price, 0, 1e6):
            errors.append("Price must be nonzero and less than $1,000,000")
        try:
            item = Item.objects.get(id=itemId)
        except Item.DoesNotExist:
            errors.append("Invalid item ID")
        if len(errors) > 0:
            raise ValidationError(errors)

        inv = Inventory.create(self, item, price)
        return inv

class OpenHour(models.Model):
    # Each OpenHours object belongs to one store, but each store has multiple OpenHours
    store = models.ForeignKey(Store)
    day = models.CharField(max_length=9)
    open_time = models.TimeField()
    close_time = models.TimeField()
    closed = models.BooleanField()

    @staticmethod
    def create(store, day, open_time, close_time, closed):
        # Validate fields
        errors = []
        if not isinstance(store, Store):
            errors.append("Invalid store object")
        if not validateStringLen(day, 1, 9):
            errors.append("Day must be valid")
        if not closed:
            if not validateHours(open_time, close_time):
                errors.append("Hours must be valid")
        if len(errors) > 0:
            raise ValidationError(errors)

        open_hour = OpenHour(store=store, day=day, open_time=open_time, close_time=close_time, closed=closed)
        open_hour.save()
        return open_hour


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
        if not validateNumOpenSet(price, 0, 1e6):
            errors.append("Price must be nonzero and less than $1,000,000")
        if len(errors) > 0:
            raise ValidationError(errors)

        inv = Inventory(store=store, item=item, price=price)
        inv.save()
        return inv

    @staticmethod
    def hasDuplicateItem(product_name, store_id):
        products = Inventory.getItemsForStore(store_id)
        for product in products:
            if product_name.lower() == product.name.lower():
                return True
        return False

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

def validateNumOpenSet(num, minimum, maximum):
    if not isinstance(num, Decimal) and not isinstance(num, float) and not isinstance(num, int):
        return False
    if num < minimum or num > maximum:
        return False
    return True

def validateHours(open_time, close_time):
    if open_time == close_time:
        return True
    if close_time > open_time:
        return True
    return False
