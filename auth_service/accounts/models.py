from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email or not phone:
            raise ValueError("Users must have an email and phone number")
        user = self.model(email=self.normalize_email(email), phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(email, phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user