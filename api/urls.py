from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('login/', views.login1, name="login-OAuth"),
    path('login/OAuth', views.login2, name="OAuth"),
    path('login/after-OAuth', views.login2, name="after-OAuth"),
]
