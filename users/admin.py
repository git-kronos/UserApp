from . models import UserProfile, UserToken
from django.contrib import admin


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserToken)