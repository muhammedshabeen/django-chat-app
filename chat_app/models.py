from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_lifecycle import LifecycleModelMixin
import requests
from django.core.files.base import ContentFile
import uuid
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, username, password=None, **extra_fields):
        """Create and save a User with the given username and password."""
        if not username:
            raise ValueError('The given email must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)




class CustomUser(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(auto_created=True,default=False)
    image  = models.ImageField(upload_to='profile_image')
    slug = models.SlugField(unique=True,null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def save_profile_pic(self, name):
        return (
            """
            https://ui-avatars.com/api/?background=0033C4&
            color=fff&size=256&name={}&rounded=true&bold=true
            """.format(name)
        )
    
    def save(self, *args, **kwargs):
        if not self.image:
            avatar_url = self.save_profile_pic(self.username)
            response = requests.get(avatar_url)
            if response.status_code == 200:
                self.image.save(f"{self.username}_avatar.png", ContentFile(response.content), save=False)
        if not self.slug:
            unique_id = str(uuid.uuid4())[:8]
            self.slug = slugify(f"{self.username}-{self.email[:5]}-{unique_id}")
        super(CustomUser, self).save(*args, **kwargs)
