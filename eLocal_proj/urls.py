from django.conf.urls import include, url
from django.contrib import admin
from eLocal_app import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

router = SimpleRouter()
router.register(r'users', views.UserViewSet, base_name='user')

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^auth/register/$', views.register, name='register'),
    url(r'^auth/logout/$', views.logout, name='logout'),
    url(r'^auth/login/$', views.login, name='login'),
    url(r'^$', views.base_render, name='base'),
]
