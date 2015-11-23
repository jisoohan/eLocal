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
    class Meta:
        unique_together = (("lat", "lng"),)
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
    image = models.ImageField(upload_to='stores/')

    def __unicode__(self):
        return self.name

class Product(models.Model):
    store = models.ForeignKey(Store)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name
