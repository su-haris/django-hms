from django.contrib import admin

# Register your models here.
from .models import UserProfile, Room, Approval

admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(Approval)
