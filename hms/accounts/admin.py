from django.contrib import admin

# Register your models here.
from .models import UserProfile, Room, Approval, Fees, NewRegistration

admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(Approval)
admin.site.register(Fees)
admin.site.register(NewRegistration)