from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, null=True, blank=True, on_delete=models.CASCADE ,default="employee")
    profile_type = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(default='user.jpg', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.profile_type}"
