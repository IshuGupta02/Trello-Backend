from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.conf.urls import include

router = DefaultRouter()
router.register(r'login', UserViewSet)

# urlpatterns= router.urls

urlpatterns = [
    path('', include(router.urls)),
    # path('', views.apiOverview, name="api-overview"),
    path('login1/', views.login1, name="login-OAuth"),
    # path('login/OAuth', views.login2, name="OAuth"),
    # path('login/after-OAuth', views.login3, name="after-OAuth"),


]

