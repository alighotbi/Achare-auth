from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator

from .manager import UserManger 


PHONE_REGEX = r"^09\d{9}$"
phone_number_regex = RegexValidator(regex=PHONE_REGEX)


class User(AbstractUser, PermissionsMixin):
    username = None
    phone_number = models.CharField(unique=True, validators=[phone_number_regex])
    is_active = models.BooleanField('active', default=True)
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    
    objects = UserManger()
