from django.conf.urls import include, url
from django.contrib import admin
from eLocal_app import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = SimpleRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'stores', views.StoreViewSet, base_name='store')
router.register(r'products', views.ProductViewSet, base_name='product')

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^auth/register/$', views.register, name='register'),
    url(r'^auth/logout/$', views.logout, name='logout'),
    url(r'^auth/login/$', views.login, name='login'),
    url(r'^$', views.base_render, name='base'),
]
urlpatterns += staticfiles_urlpatterns()