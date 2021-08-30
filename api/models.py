"""
All models used in trello-backend
"""

from django.db import models
from ckeditor.fields import RichTextField

class User(models.Model):
    """
    User details: 
    all registered users' details

    e.g.
    enrollment number- 20114041
    User_name- Ishu Gupta
    admin- False
    enabled- True
    token=""    
    """
    enrollment_no = models.IntegerField(primary_key=True)
    User_name = models.CharField(max_length=100)
    admin= models.BooleanField()
    enabled= models.BooleanField()
    token= models.CharField(max_length=200)

class Project(models.Model):
    """
    Project details:
    information about all ongoing projects

    e.g.
    id-"1"
    Project_name- "Noticeboard"
    wiki- ""
    due_date- "24/10/2022"
    members- 1,2,3
    admins- 2,3
    """
    id = models.IntegerField(primary_key=True)
    Project_name = models.CharField(max_length=100)
    wiki= RichTextField()
    due_date= models.DateField()
    members= models.ManyToManyField(User, related_name="member")
    admins= models.ManyToManyField(User, related_name="admins_Project")

class List(models.Model):
    """
    List details:
    all lists like todo, doing, done, etc added in projects

    e.g.
    id-"1"
    List_name- "todo"
    Project- 1
    """
    id=models.IntegerField(primary_key=True)
    List_name = models.CharField(max_length=100)
    Project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

class Card(models.Model):
    """
    Card details:
    details of all cards corresponding to every list

    e.g.
    id-"1"
    Card_name- "Make views"
    List- 1
    assigned- 1,2
    description-"complete views of trello app"
    """
    id= models.IntegerField(primary_key=True)
    Card_name = models.CharField(max_length=100)
    List = models.ForeignKey(to=List, on_delete=models.CASCADE)
    assigned= models.ManyToManyField(User)
    description = models.CharField(max_length=500)

class Comment(models.Model):
    """
    Comments added on Cards:
    all the comments added of any card

    e.g.
    id-1
    User- 1
    Card- 2
    Comment- "make sure to use pylint"
    """
    id= models.IntegerField(primary_key=True)
    User= models.ForeignKey(to=User, on_delete=models.CASCADE)
    Card= models.ForeignKey(to=Card, on_delete=models.CASCADE)
    Comment=models.CharField(max_length=100)
