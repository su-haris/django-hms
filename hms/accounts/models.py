
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Room(models.Model):
    no = models.CharField(max_length=5, default=None)

    room_choice = [('S', 'Single Room'), ('D', 'Double Room'), ('T', 'Triple Room')]
    room_type = models.CharField(choices=room_choice, max_length=1, default=None)
    vacant = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    present = models.PositiveIntegerField(validators=[MaxValueValidator(4)])

    def __str__(self):
        return self.no


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, blank=True, null=True, unique=False)
    location = models.CharField(max_length=10)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    dob = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True, blank=True
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



