
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Room(models.Model):
    no = models.CharField(max_length=5)

    room_choice = [('S', 'Single Room'), ('D', 'Double Room'), ('T', 'Triple Room')]
    room_type = models.CharField(choices=room_choice, max_length=1, default=None)
    vacant = models.BooleanField(default=False)
    capacity = models.IntegerField()
    present = models.IntegerField()

    def __str__(self):
        return self.no


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, blank=True, null=True, unique=False)
    location = models.CharField(max_length=10)
    age = models.IntegerField()
    dob = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True
    )
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True
    )
    room_allotted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



