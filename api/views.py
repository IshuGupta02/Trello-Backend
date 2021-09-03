"""
Contains all views
"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
import json
import requests
from .login_config import config
from . import models
from django.contrib.auth import login, logout
from rest_framework import viewsets
from .serializers import UserSerializer,ProjectSerializer,ListSerializer,CardSerializer,CommentSerializer
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions like login, logout
    """
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, url_path='login')
    def login1(req):
        """
        It will redirect to oauth page
        from /api/login--> oauth
        """
        print("login1")
        url = f"https://channeli.in/oauth/authorise/?client_id={config['CLIENT_ID']}&redirect_uri={config['REDIRECT_URI']}&state={config['STATE_STRING']}"
        return HttpResponseRedirect(url)

    @action(detail=True, url_path='login/OAuth')
    def login2(req):
        """
        exchange auth_code (received after login through channeli) with access_token which is further used to get the user's data
        """
        try:
            auth_code = req.GET['code']

        except:
            return HttpResponseBadRequest()

        params = {
            'client_id': config['CLIENT_ID'],
            'client_secret': config['CLIENT_SECRET'],
            'grant_type': 'authorization_code',
            'redirect_uri': config['REDIRECT_URI'],
            'code': auth_code,
        }

        res = requests.post("https://channeli.in/open_auth/token/", data=params)

        if (res.status_code == 200):
            access_token = res.json()['access_token']
            refresh_token = res.json()['refresh_token']
        else:
            return HttpResponseBadRequest()

        header = {
            "Authorization": "Bearer " + access_token,
        }

        res1 = requests.get("https://channeli.in/open_auth/get_user_data/", headers=header)
        data_final = res1.json()

        isMaintainer = False
        for role in data_final['person']['roles']:
            print(role['role'])
            if (role['role'] == 'Maintainer'):
                isMaintainer = True

        if not isMaintainer:
            return HttpResponse("You are not a maintainer")

        try:
            user = models.User.objects.get(enrollment_no=data_final['username'])

        except:
            user_name = data_final['person']['fullName']
            ern = data_final['username']
            isAdmin = False
            isEnabled = True
            user = models.User(enrollment_no=ern, User_name=user_name, admin=isAdmin, enabled=isEnabled)
            print("saving")
            user.save()
            print("saved")
        login(request=req, user=user)
        return HttpResponse("all okay!")



def login1(req):
    """
    It will redirect to oauth page
    from /api/login--> oauth
    """
    print("login1")
    url = f"https://channeli.in/oauth/authorise/?client_id={config['CLIENT_ID']}&redirect_uri={config['REDIRECT_URI']}&state={config['STATE_STRING']}"
    return HttpResponseRedirect(url)

def login2(req):
    """
    exchange auth_code (received after login through channeli) with access_token which is further used to get the user's data
    """
    try:
        auth_code= req.GET['code']

    except:
        return HttpResponseBadRequest()

    params={
        'client_id':config['CLIENT_ID'],
        'client_secret': config['CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'redirect_uri':config['REDIRECT_URI'],
        'code':auth_code,
    }

    res = requests.post("https://channeli.in/open_auth/token/", data=params)

    if (res.status_code == 200):
        access_token=res.json()['access_token']
        refresh_token= res.json()['refresh_token']
    else:
        return HttpResponseBadRequest()

    header={
        "Authorization": "Bearer "+access_token,
    }

    res1 = requests.get("https://channeli.in/open_auth/get_user_data/", headers=header)
    data_final=res1.json()

    isMaintainer=False
    for role in data_final['person']['roles']:
        print(role['role'])
        if(role['role'] == 'Maintainer'):
            isMaintainer=True

    if not isMaintainer:
        return HttpResponse("You are not a maintainer")

    try:
        user=models.User.objects.get(enrollment_no=data_final['username'])

    except:
        user_name=data_final['person']['fullName']
        ern=data_final['username']
        isAdmin = False
        isEnabled = True
        user = models.User(enrollment_no= ern, User_name= user_name, admin= isAdmin, enabled= isEnabled)
        print("saving")
        user.save()
        print("saved")
    login(request=req, user=user)
    return HttpResponse("all okay!")

def login3(req):
    """
    after oauth
    """
    pass