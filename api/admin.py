# Register your models here.

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(List)
admin.site.register(Card)
admin.site.register(Comment)