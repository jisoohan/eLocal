from django.conf.urls import patterns, include, url
from django.contrib import admin

from eLocal_app import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^stores/search', views.searchStore),
    url(r'^stores/add', views.addStore),
    url(r'^stores', views.storeSearchPage),
    url(r'^products/search', views.searchProduct),
    url(r'^products/add', views.addProduct),
    url(r'^products', views.productSearchPage),
    url(r'^cart/remove/product=(?P<product_id>\d+)&store=(?P<store_id>\d+)', views.removeCart),
    url(r'^cart/add/product=(?P<product_id>\d+)&store=(?P<store_id>\d+)', views.addCart),
    url(r'^cart', views.shoppingPage),
    url(r'^', views.homePage),
]
