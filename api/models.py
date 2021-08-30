from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class user(models.Model):
    enrollment_no = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100)
    admin= models.BooleanField()
    enabled= models.BooleanField()
    token= models.CharField(max_length=200)

class project(models.Model):
    id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=100)
    wiki= RichTextField()
    due_date= models.DateField()
    members= models.ManyToManyField(user, related_name="member")
    admins= models.ManyToManyField(user, related_name="admins_project")

class list(models.Model):
    id=models.IntegerField(primary_key=True)
    list_name = models.CharField(max_length=100)
    project = models.ForeignKey(to=project, on_delete=models.CASCADE)

class card(models.Model):
    id= models.IntegerField(primary_key=True)
    card_name = models.CharField(max_length=100)
    list = models.ForeignKey(to=list, on_delete=models.CASCADE)
    assigned= models.ManyToManyField(user)
    description = models.CharField(max_length=500)

class comment(models.Model):
    id= models.IntegerField(primary_key=True)
    user= models.ForeignKey(to=user, on_delete=models.CASCADE)
    card= models.ForeignKey(to=card, on_delete=models.CASCADE)
    comment=models.CharField(max_length=100)
