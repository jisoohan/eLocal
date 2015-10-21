from django.db import models
from django.core.exceptions import ValidationError
from time import time

# Adapted from https://stackoverflow.com/questions/8128143/any-existing-solution-to-implement-opening-hours-in-django
WEEKDAYS = [
  (0, _("Sunday")),
  (1, _("Monday")),
  (2, _("Tuesday")),
  (3, _("Wednesday")),
  (4, _("Thursday")),
  (5, _("Friday")),
  (6, _("Saturday"))
]


class Item(models.Model):
    name = models.CharField(max_length=128)
    # Stores can be accessed using <item>.store_set


class Store(models.Model):
    name      = models.CharField(max_length=128)
    address   = models.CharField(max_length=256)
    latitude  = models.FloatField()
    longitude = models.FloatField()
    # Hours can be accessed using <store>.openhours_set
    items     = models.ManyToManyField(Item, though='Inventory')


# Adapted from https://stackoverflow.com/questions/8128143/any-existing-solution-to-implement-opening-hours-in-django
class OpenHours(models.Model):
    # Each OpenHours object belongs to one store, but each store has multiple OpenHours
    store     = models.ForeignKey(Store)
    weekday   = models.IntegerField(choices=WEEKDAYS, unique=True)
    is_open   = models.BooleanField()
    from_hour = models.TimeField()
    to_hour   = models.TimeField()


class Inventory(models.Model):
    store = models.ForeignKey(Store)
    item = models.ForeignKey(Item)
    # Using DecimalField instead of FloatField here to enforce precision of prices (i.e. $123.45)
    price = models.DecimalField()


