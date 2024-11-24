from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):

    ROLE_CHIOCES = [
        ("ADMIN","Admin"),('USER','User')
    ]

    username = models.CharField(max_length=80,unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=80,choices=ROLE_CHIOCES)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    objects = UserManager()
    
    # creating JWt manually
    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def __str__(self):
        return self.username
    

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    user = models.ForeignKey(User,related_name='tickets',null=True,on_delete=models.SET_NULL)
    event = models.ForeignKey(Event,related_name='tickets',on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}--{self.event}'
