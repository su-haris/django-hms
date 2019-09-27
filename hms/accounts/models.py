from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
