from django.db import models

from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

import uuid


class MyAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username , password = None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        if not username:
            raise ValueError(('The username must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)

        user.save(using=self._db)
        # user.save()
        return user

    def create_superuser(self, email, username, password =None):
        """
        Create and save a SuperUser with the given email and password.
        """

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.is_admin=True
        user.is_active =True
        user.is_staff=True
        user.is_superuser=True
        # user.save()
        user.save(using=self._db)

        return user

def get_profile_image_filepath(self, filename):
    # return f'profile_images/{self.pk}/{"profile_image.png"}'
    return f'profile_images/{self.pk}/{filename}'

def get_default_profile_image():
    return "account/blank.png"


class Account(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(verbose_name="email" , max_length=60 , unique=True ,)
    username=models.CharField(max_length=30 , unique=True)
    date_joined=models.DateTimeField(verbose_name="date joined" , auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login" , auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    profile_image=models.ImageField(max_length=255 , upload_to=get_profile_image_filepath, null=True , blank=True , default=get_default_profile_image,)
    hide_email=models.BooleanField(default=True)

    objects=MyAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # [str(self.profile_image).index(f'profile_images/{self.pk}/'): 1]
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self , perm , obj=None):
        return self.is_admin

    def has_module_perms(self , app_label):
        return True