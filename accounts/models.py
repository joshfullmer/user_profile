from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    date_of_birth = models.DateField()
    bio = models.TextField()
    avatar = models.ImageField(upload_to='./avatars')
    hobbies = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)
