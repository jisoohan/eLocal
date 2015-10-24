from django.conf.urls import patterns, include, url
from django.contrib import admin

from eLocal_app import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^products', views.productSearchPage),
    url(r'^shopping', views.shoppingPage),
    url(r'^stores', views.storeSearchPage), #improve later to take into account store ID
    url(r'^addstore', views.addStore),
    url(r'^addproduct', views.addProduct),
    url(r'^', views.homePage),
]
