from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Address(models.Model):
    st_number = models.CharField(max_length=10)
    st_name = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    country = models.CharField(max_length=2)
    lat = models.FloatField()
    lng = models.FloatField()

    def __unicode__(self):
        return '{0} {1}, {2}, {3} {4}'.format(self.st_number, self.st_name, self.city, self.state, self.zipcode)

class Store(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    has_card = models.BooleanField()
    address = models.OneToOneField(Address)

    def __unicode__(self):
        return self.name

'''
from django.db import models
from django.core.exceptions import ValidationError
from time import time
from datetime import time as TimeOfDay
from decimal import *

class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    # Stores can be accessed using <item>.store_set

    @staticmethod
    def create(name, description):
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
        return list(Item.objects.filter(name__icontains=name))

    @staticmethod
    def updateProductCheck(product, product_list, product_name, description):
        if product.name == product_name and product.description == description:
            return False
        if product.name == product_name and product.description != description:
            return True
        for product_item in product_list:
            if product_item['name'] == product_name:
                return False
        return True

    # Associates this item with a corresponding store and price
    def addToStore(self, storeId, price):
        store = None
        try:
            store = Store.objects.get(id=storeId)
        except Store.DoesNotExist:
            raise ValidationError(["Invalid store ID"])
        inv = Inventory.create(store, self, price)
        return inv

    def clean_fields(self, exclude=None):
        errors = []
        if not validateStringLen(self.name, 1, 128):
            errors.append("Item name must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(self.description, 1, 1024):
            errors.append("Item description must be a non-empty string 1 to 1024 characters long")
        if len(errors) > 0:
            raise ValidationError(errors)

    def clean(self):
        pass

    def validate_unique(self, exclude=None):
        pass

    def save(self):
        self.full_clean()
        super(Item, self).save()



class Store(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    country = models.CharField(max_length=2)
    has_card = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # Hours can be accessed using <store>.openhour_set
    items = models.ManyToManyField(Item, through='Inventory')

    @staticmethod
    def create(name, address, city, state, zip_code, country, has_card, latitude, longitude):
        #if Store.hasDuplicate(name, address, city, state, zip_code, country, has_card):
        #    errors.append("A matching store already exists")
        #if len(errors) > 0:
        #    raise ValidationError(errors)

        store = Store(name=name, address=address, city=city, state=state, zip_code=zip_code,
                      country=country, has_card=has_card, latitude=latitude, longitude=longitude)
        store.save()
        return store

    @staticmethod
    def hasDuplicate(name, address, city, state, zip_code, country, has_card):
        return Store.objects.filter(name__iexact=name, address__iexact=address, city__iexact=city,
                                    state__iexact=state, zip_code__iexact=zip_code).exists()

    @staticmethod
    def updateStoreCheck(store, name, address, city, state, zip_code, country, has_card):
        if store.name == name and store.address == address and store.city == city and store.state == state and store.zip_code == zip_code and store.country == country and store.has_card == has_card:
            return False
        if Store.hasDuplicate(name, address, city, state, zip_code, country, has_card):
            if store.id ==  Store.objects.get(name=name, address=address, city=city, state=state, zip_code=zip_code).id:
                return True
            else:
                return False
        return True

    # Get a list of stores whose names match the query string
    @staticmethod
    def getStores(name):
        # Validate field
        errors = []
        if not validateStringLen(name, 1, 128):
            errors.append("Store name must be a non-empty string 1 to 128 characters long")
        if len(errors) > 0:
            raise ValidationError(errors)

        #name = name.strip()
        return list(Store.objects.filter(name__icontains=name))

    # Associates this store with a corresponding item and price
    def addItem(self, itemId, price):
        item = None
        try:
            item = Item.objects.get(id=itemId)
        except Item.DoesNotExist:
            raise ValidationError(["Invalid item ID"])
        inv = Inventory.create(self, item, price)
        return inv

    def clean_fields(self, exclude=None):
        errors = []
        if not validateStringLen(self.name, 1, 128):
            errors.append("Name must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(self.address, 1, 256):
            errors.append("Address must be a non-empty string 1 to 128 characters long")
        if not validateStringLen(self.city, 1, 60):
            errors.append("City must be a non-empty string 1 to 60 characters long")
        if not validateStringLen(self.state, 2, 2):
            errors.append("State must be a non-empty string 2 characters long")
        if not validateStringLen(self.zip_code, 5, 5):
            errors.append("Zipcode must be a non-empty string 5 characters long")
        if not validateStringLen(self.country, 2, 2):
            errors.append("Country must be a non-empty string 2 characters long")
        if not isinstance(self.has_card, bool):
            errors.append("Has_card must be either true or false")
        if not validateNumClosedSet(self.latitude, -90, 90):
            errors.append("Latitude must be between -90 and 90")
        if not validateNumClosedSet(self.longitude, -180, 180):
            errors.append("Longitude must be between -180 and 180")
        if len(errors) > 0:
            raise ValidationError(errors)

    def clean(self):
        pass

    def validate_unique(self, exclude=None):
        pass

    def save(self):
        self.full_clean()
        super(Store, self).save()



class OpenHour(models.Model):
    # Each OpenHours object belongs to one store, but each store has multiple OpenHours
    store = models.ForeignKey(Store)
    day = models.CharField(max_length=9)
    open_time = models.TimeField()
    close_time = models.TimeField()
    closed = models.BooleanField()

    @staticmethod
    def create(store, day, open_time, close_time, closed):
        open_hour = OpenHour(store=store, day=day, open_time=open_time, close_time=close_time, closed=closed)
        open_hour.save()
        return open_hour

    def clean_fields(self, exclude=None):
        errors = []
        if not validateStringLen(self.day, 1, 9):
            errors.append("Day must be valid")
        if not isinstance(self.store, Store):
            errors.append("Invalid store object")
        if not self.closed:
            if not validateHours(self.open_time, self.close_time):
                errors.append("Hours must be valid")
        if len(errors) > 0:
            raise ValidationError(errors)

    def clean(self):
        pass

    def validate_unique(self, exclude=None):
        pass

    def save(self):
        self.full_clean()
        super(OpenHour, self).save()



# Tracks item-store-price associations
class Inventory(models.Model):
    store = models.ForeignKey(Store)
    item  = models.ForeignKey(Item)
    # Using DecimalField instead of FloatField here to enforce precision of prices (i.e. $123.45)
    price = models.DecimalField(decimal_places=2, max_digits=8)

    @staticmethod
    def create(store, item, price):
        if isinstance(price, float) or isinstance(price, int):
            price = Decimal(price)
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

    def clean_fields(self, exclude=None):
        errors = []
        if not isinstance(self.store, Store):
            errors.append("Invalid store object")
        if not isinstance(self.item, Item):
            errors.append("Invalid item object")
        if not validateNumOpenSet(self.price, 0, 1e6):
            errors.append("Price must be nonzero and less than $1,000,000")
        if len(errors) > 0:
            raise ValidationError(errors)

    def clean(self):
        pass

    def validate_unique(self, exclude=None):
        pass

    def save(self):
        self.full_clean()
        super(Inventory, self).save()


def validateStringLen(string, min_len, max_len):
    return isinstance(string, str) and min_len <= len(string) <= max_len

def validateNumOpenSet(num, minimum, maximum):
    if not isinstance(num, Decimal) and not isinstance(num, float) and not isinstance(num, int):
        return False
    return minimum < num < maximum

def validateNumClosedSet(num, minimum, maximum):
    if not isinstance(num, Decimal) and not isinstance(num, float) and not isinstance(num, int):
        return False
    return minimum <= num <= maximum

def validateHours(open_time, close_time):
    return isinstance(open_time, TimeOfDay) and isinstance(close_time, TimeOfDay) and close_time >= open_time
'''
