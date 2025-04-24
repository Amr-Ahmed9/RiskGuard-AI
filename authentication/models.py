
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('personal', 'Personal Finance'),
        ('business', 'Business')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='personal')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
