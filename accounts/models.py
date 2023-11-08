# from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# class UserManager(BaseUserManager):
#     def create_user(self, email, full_name, profile_picture=None, gender=None, password=None, is_admin=False, is_staff=False, is_active=True):
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#         if not full_name:
#             raise ValueError("User must have a full name")
#
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.full_name = full_name
#         user.set_password(password)  # change password to hash
#         # user.profile_picture = profile_picture
#         user.gender = gender
#         user.admin = is_admin
#         user.profile_picture = profile_picture
#         user.staff = is_staff
#         user.active = is_active
#         user.save(using=self._db)
#         return user
#
#     def create_staffuser(self, email, profile_picture, gender, full_name, password=None):
#         user = self.create_user(
#             email,
#             full_name,
#             profile_picture,
#             gender,
#             password=password,
#             is_staff=True,
#         )
#         return user
#
#     def create_superuser(self, email, password=None):
#         user = self.create_user(
#             email,
#             password=password,
#             is_staff=True,
#             is_admin=True,
#         )
#         return user

class User(AbstractUser):
    email = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
    username = models.CharField(max_length=10)
    # objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

# def get