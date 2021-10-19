"""
Contains all views
"""
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
import json
import requests
from rest_framework.response import Response
from .login_config import config
from . import models
from django.contrib.auth import login, logout
from rest_framework import viewsets
from .serializers import UserSerializer,ProjectSerializer,ListSerializer,CardSerializer,CommentSerializer, ProjectSerializer1, CardSerializer1
from rest_framework.decorators import action
from rest_framework.views import APIView
from .permissions import IsUserEnabled, IsAdminOrProjectAdminOrReadOnly, IsAdmin, IsOwnerOrReadOnly, IsTeamMemberOrReadOnly_List, IsTeamMemberOrReadOnly_Project, IsTeamMemberOrReadOnly_Card, Not_allowed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

@api_view(['GET'])
def check(request):
    """
    checks whether or not a user is logged in
    """
    # print("print1")
    # if(request.user.is_authenticated):
    #     print("print2")
    #     res= Response({'status': 'loggedIn'}, status=status.HTTP_202_ACCEPTED)
    # else:
    #     print("print3")
    #     res= Response({'status': 'NotloggedIn'}, status=status.HTTP_202_ACCEPTED)

    # print("print4")
    # res['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
    # res['Access-Control-Allow-Credentials']='true'
    # print("print5")
    # return res

    msg = {
        "loggedin": False
    }
    if request.user.is_authenticated:
        msg["loggedin"] = True
        res = Response(msg, status=status.HTTP_202_ACCEPTED)
        res['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
        res['Access-Control-Allow-Credentials'] = 'true'
        return res
    else:
        res = Response(msg, status=status.HTTP_202_ACCEPTED)
        res['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
        res['Access-Control-Allow-Credentials'] = 'true'
        return res

class LoginViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions like login, logout
    1. if user exists--> login
    2. if new user comes--> create a new User Object and login
    3. logout
    """
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path='login', url_name='login-login')
    def login1(self, req):
        """
        It will redirect to oauth page
        from /api/login--> oauth
        """
        print("login1")
        url = f"https://channeli.in/oauth/authorise/?client_id={config['CLIENT_ID']}&redirect_uri={config['REDIRECT_URI']}&state={config['STATE_STRING']}"
        return HttpResponseRedirect(url)

    @action(detail=False, url_path='OAuth', url_name='login-OAuth')
    def login2(self, req):
        """
        exchange auth_code (received after login through channeli) with access_token which is further used to get the user's data
        """
        try:
            auth_code = self.request.query_params.get('code')
            print(auth_code)
            # auth_code = self.request.query_params.get('code')

        except:
            print("bad1")
            return HttpResponseBadRequest()

        # print("print1")
        params = {
            'client_id': config['CLIENT_ID'],
            'client_secret': config['CLIENT_SECRET'],
            'grant_type': 'authorization_code',
            'redirect_uri': config['REDIRECT_URI'],
            'code': auth_code,
        }

        # print("print2")
        res = requests.post("https://channeli.in/open_auth/token/", data=params)

        # print("print3")

        # print("print3_next_before")

        if (res.status_code == 200):
            access_token = res.json()['access_token']
            refresh_token = res.json()['refresh_token']
        else:
            print("bad")
            return HttpResponseBadRequest()

        # print("print3_next")
        header = {
            "Authorization": "Bearer " + access_token,
        }

        # print("print4")

        res1 = requests.get("https://channeli.in/open_auth/get_user_data/", headers=header)
        data_final = res1.json()

        isMaintainer = False
        active=True
        for role in data_final['person']['roles']:
            print(role['role'])
            if (role['role'] == 'Maintainer'):
                isMaintainer = True
                # if(role['activeStatus']!='ActiveStatus.IS_ACTIVE'):
                #     active=False

        print(data_final)

        # if not active:
        #     try:
        #         models.User.objects.filter(enrollment_no=data_final['username']).delete()
        #     except:
        #         error=True
        #     return JsonResponse({'status': 'you are not active anymore'})

        if not isMaintainer:
            return JsonResponse({'status': 'you are not a maintainer'})

        print(data_final)

        try:
            user = models.User.objects.get(enrollment_no=data_final['username'])

        except:
            print("saving data")
            username= data_final['username']
            user_name = data_final['person']['fullName']
            email_id=data_final['contactInformation']['emailAddress']
            ern = data_final['username']
            isAdmin = False
            isEnabled = True
            profile_url=data_final['person']['displayPicture']
            user = models.User(enrollment_no=ern, User_name=user_name, admin=isAdmin, enabled=isEnabled, email=email_id, profile=profile_url, username=username)
            print("saving")
            user.save()
            print("saved")
        login(request=req, user=user)

        print(req.auth)
        print(req.user)
        print(req.user.is_authenticated)

        info={
            'data':'Done!', 
            'isAdmin':user.admin , 
            'isEnabled' : user.enabled
        }

        res= Response(info, status=status.HTTP_202_ACCEPTED)
        res['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
        res['Access-Control-Allow-Credentials']='true'
        # res['withCredentials']='true'

        # res['Access-Control-Expose-Headers']='*'

        # access-control-expose-headers: Set-Cookie
        return res

        # return Response({'data':'Done!', 'isAdmin':user.admin , 'isEnabled' : user.enabled},status=status.HTTP_202_ACCEPTED)
        # return HttpResponse("done!")

    @action(methods=['GET'], detail=False, url_path='logout', url_name='login-logout')
    def logout_(self, request):
        """
        logout user
        """
        if request.user.is_authenticated:
            logout(request)
            res= Response({'status': 'successful'}, status=status.HTTP_202_ACCEPTED)
            res['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
            res['Access-Control-Allow-Credentials']='true'
            # return JsonResponse({'status': 'successful'})
            return res
        else:
            return HttpResponseForbidden()

class UserViewSet(viewsets.ModelViewSet):
    """
    1. get all users data
    2. update a user's Admin Status
    3. update a user's Enabled Status
    """
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    # @action(methods= ['GET'], detail=False, url_path='myprojects', url_name='user-myprojects')
    # def projects(self, request):
    #     print(request.user)
    #     projects_data=ProjectSerializer(request.user.member.all(), many=True)
    #     return Response(projects_data.data)

    # @action(methods= ['GET'],detail=False, url_path='mycards', url_name='user-mycards')
    # def cards(self, request):
    #     cards_data=CardSerializer(request.user.mycards.all(), many=True)
    #     return Response(cards_data.data)
    def dispatch(self, *args, **kwargs):
        response = super(UserViewSet, self).dispatch(*args, **kwargs)
        response['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
        response['Access-Control-Allow-Credentials']='true'
        return response

    def get_permissions(self):
        """
        everbody can get details of users but only admins can enable/disable, change to admin/remove from admin
        """
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        elif self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = [Not_allowed]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsAdmin]
        return super(UserViewSet, self).get_permissions()

    @action(methods=['GET'], detail=False, url_path='info', url_name='user-info')
    def info(self, request):
        # print(request.user)
        # # user_data=models.User.objects.get(request.user)
        # return Response("user")

        # print("1")

        info = UserSerializer(request.user)
        # return Response(info.data)

        # print("2")

        res= Response(info.data, status=status.HTTP_202_ACCEPTED)
        res['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
        res['Access-Control-Allow-Credentials']='true'

        # print("3")

        return res

        # {headers:{"Access-Control-Request-Headers": "x-requested-with", mode: "cors"}}
        # , headers={"Access-Control-Allow-Headers": "*"}

class ProjectViewSet(viewsets.ModelViewSet):
    """
    1. get all projects
    2. update a project- members, admins, wiki, project_name, due_date
    3. delete a project
    4. create new project
    """
    queryset = models.Project.objects.all()
    serializer_class = ProjectSerializer

    # @action(methods=['GET'], detail=False, url_path='list', url_name='project-list')
    # def list_project(self, request):
    #     proj= models.Project.objects.all()
    #     proj_data=ProjectSerializer(proj, many=True)
    #     return Response(proj_data.data)
    #
    # @action(methods=['POST'], detail=False, url_path='create', url_name='project-create')
    # def create_project(self, request):
    #     proj_data=ProjectSerializer(proj, many=True)
    #     return Response(proj_data.data)

    # def perform_create(self, serializer):
    #     serializer.save()

    def dispatch(self, *args, **kwargs):
        response = super(ProjectViewSet, self).dispatch(*args, **kwargs)
        response['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
        response['Access-Control-Allow-Credentials']='true'

        return response

    def get_permissions(self):
        """
        1. everyone can get information about any project or create a new project
        2. only project admins or app admins can add or remove members, project_admins, change due_date, edit wiki, etc
        """
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsAdminOrProjectAdminOrReadOnly]
        return super(ProjectViewSet, self).get_permissions()

class ListViewSet(viewsets.ModelViewSet):
    """
    1. get all lists
    2. create a new list in a project
    3. update a list- list_name
    4. delete a list
    """
    queryset = models.List.objects.all()
    serializer_class = ListSerializer

    def get_permissions(self):
        """
        anyone can get information about any list
        only project members can create/update/delete a list
        """
        if self.request.method == 'GET':
            print("get")
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            print("NOTget")
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsTeamMemberOrReadOnly_List]

        return super(ListViewSet, self).get_permissions()

class CardViewSet(viewsets.ModelViewSet):
    """
    1. get all cards
    2. create a new card in a project
    3. update a card- card_name, assigned_to,description
    4. delete a card
    """

    queryset = models.Card.objects.all()
    serializer_class = CardSerializer

    def get_permissions(self):
        """
        anyone can get information about any card
        only project members can create/update/delete a card
        """
        print("checking perms")
        if self.request.method == 'GET':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsTeamMemberOrReadOnly_Card]
            # self.permission_classes = [IsTeamMemberOrReadOnly_Card]
            # self.permission_classes = [IsAuthenticated,IsUserEnabled]


        # print("checked perms")
        return super(CardViewSet, self).get_permissions()

class CommentViewSet(viewsets.ModelViewSet):
    """
    1. get all comments
    2. update a comment
    3. create a comment
    """

    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        everyone can view comments/ create a new comment
        only comment creator can change it
        """
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsUserEnabled, IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated,IsUserEnabled, IsOwnerOrReadOnly]
        return super(CommentViewSet, self).get_permissions()


class ProjectDataViewSet(viewsets.ModelViewSet):
    """
    1. get all projects
    2. update a project- members, admins, wiki, project_name, due_date
    3. delete a project
    4. create new project
    """
    queryset = models.Project.objects.all()
    serializer_class = ProjectSerializer1

    def dispatch(self, *args, **kwargs):
        response = super(ProjectDataViewSet, self).dispatch(*args, **kwargs)
        response['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
        response['Access-Control-Allow-Credentials']='true'

        return response

class CardDataViewSet(viewsets.ModelViewSet):
    """
    1. get all cards
    2. create a new card in a project
    3. update a card- card_name, assigned_to,description
    4. delete a card
    """

    queryset = models.Card.objects.all()
    serializer_class = CardSerializer1

class CardCommentsViewSet(viewsets.ModelViewSet):
    """
    1. get all comments and basic details of a card
    """

    queryset = models.Card.objects.all()
    serializer_class = CardCommentSerializer

    def dispatch(self, *args, **kwargs):
        response = super(CardCommentsViewSet, self).dispatch(*args, **kwargs)
        response['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
        response['Access-Control-Allow-Credentials']='true'

        return response


# comments using websockets example
def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })


# email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


@api_view(['GET','POST'])
def success(request):
    
    print("data: ", request.data)

     card= request.data['Card']
    list1= request.data['list']
    project= request.data['project']
    email= request.data['email']

    
    template= render_to_string('email_template.html', {'card': card, 'list': list1, 'project': project })
   
    email=EmailMessage(
        'TRELLO | new card assigned',
        template,
        settings.EMAIL_HOST_USER,
        email
    )

    email.fall_silently=False
    email.send()

    res= Response({'done': 'true'}, status=status.HTTP_202_ACCEPTED)
    res['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
    res['Access-Control-Allow-Credentials']='true'
    return res
    # {
    #     "card": "card1",
    #     "list":"list1",
    #     "email":["ishugupta0298@gmail.com"],
    #     "project":"none"
    # }

