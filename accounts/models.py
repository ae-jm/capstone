# # from django.core.validators import MaxValueValidator
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#
# class UserManager(BaseUserManager):
#     def create_user(self, email, username, first_name, last_name, password=None):
#         #, is_admin = False, is_staff = False, is_active = True
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#         if not username:
#             raise ValueError("User must have a username")
#         # if not first_name:
#         #     raise ValueError("User must have a username")
#         # if not last_name:
#         #     raise ValueError("User must have a username")
#
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#         )
#
#         user.set_password(password)  # change password to hash
#         # user.admin = is_admin
#         # user.profile_picture = profile_picture
#         # user.staff = is_staff
#         # user.active = is_active
#         user.save(using=self._db)
#         return user
#
#     def create_staffuser(self, email, username, first_name, last_name, password=None):
#         user = self.create_user(
#             email,
#             username,
#             first_name,
#             last_name,
#             password=password,
#         )
#         user.is_staff = True
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, username, first_name, last_name, password=None):
#         user = self.create_user(
#             email,
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             password=password,
#         )
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
# class User(AbstractBaseUser):
#     email = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
#     username = models.CharField(max_length=10, unique=True)
#     first_name = models.CharField(max_length=5)
#     last_name = models.CharField(max_length=20)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     @property
#     def is_staff(self):
#         return self.is_staff
#
#     @property
#     def is_admin(self):
#         return self.is_admin
#

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    username = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=5)
    last_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
