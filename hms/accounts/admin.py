from django.contrib import admin

# Register your models here.
from .models import UserProfile, Room

admin.site.register(UserProfile)
admin.site.register(Room)
