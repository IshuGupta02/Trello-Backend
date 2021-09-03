from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', UserViewSet)
urlpatterns= router.urls

# urlpatterns = [
#     # path('', views.apiOverview, name="api-overview"),
#     # path('login/', views.login1, name="login-OAuth"),
#     # path('login/OAuth', views.login2, name="OAuth"),
#     # path('login/after-OAuth', views.login3, name="after-OAuth"),
#
#
# ]

