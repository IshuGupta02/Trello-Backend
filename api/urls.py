from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import LoginViewSet, UserViewSet, ProjectViewSet, ListViewSet, CardViewSet, CommentViewSet, check, ProjectDataViewSet, CardDataViewSet, success
from django.conf.urls import include
from . import views

router = DefaultRouter()
router.register(r'login', LoginViewSet)
router.register(r'project', ProjectViewSet)
router.register(r'user', UserViewSet)
router.register(r'list', ListViewSet)
router.register(r'card', CardViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'projectData', ProjectDataViewSet)
router.register(r'cardData', CardDataViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
    path('check/', check, name='check_login'),
    path('success/', success, name='success'),
    path('<str:room_name>/', views.room, name='room'),
    # path('', views.apiOverview, name="api-overview"),
    # path('login1/', views.login1, name="login-OAuth"),
    # path('login/OAuth', views.login2, name="OAuth"),
    # path('login/after-OAuth', views.login3, name="after-OAuth"),
    # path('hello/myprojects/', views.myprojects, name="myprojects"),

    path('', views.index, name='index'),
    
]

