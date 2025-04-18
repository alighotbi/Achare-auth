from django.db import models

from django.contrib.auth.models import BaseUserManager


class UserManger(BaseUserManager):
    def create_user(self, phone_number, password=None, is_active=True):
        if not phone_number:
            raise ValueError("Users must have an phone")
        # if not password:
        #     raise ValueError("Users must have an password")

        user = self.model(phone_number=phone_number)
        # user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

    

    