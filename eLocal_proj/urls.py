from django.conf.urls import patterns, include, url
from django.contrib import admin

from eLocal_app import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^addproduct', views.addProduct),
    url(r'^addstore', views.addStore),
    url(r'^products', views.productSearchPage),
    url(r'^searchproduct', views.searchProduct),
    url(r'^searchstore', views.searchStore),
    url(r'^shopping', views.shoppingPage),
    url(r'^stores', views.storeSearchPage), #improve later to take into account store ID
    url(r'^', views.homePage),
]
