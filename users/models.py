from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, first_name, last_name, **extra_fields):
        if not username:
            raise ValueError(_("The username must be set"))
        if not first_name:
            raise ValueError(_("The first name must be set"))
        if not last_name:
            raise ValueError(_("The last name must be set"))
        
        user = self.model(username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        return self.create_user(username, password, first_name, last_name, **extra_fields)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return '(' + self.username + ') ' + self.first_name + ' ' + self.last_name 