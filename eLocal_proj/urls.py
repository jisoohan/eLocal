from django.conf.urls import patterns, include, url
from django.contrib import admin

from eLocal_app import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', views.homepage),
]
