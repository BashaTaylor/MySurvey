from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import re

class CustomUserManager(BaseUserManager):
    def register_validator(self, postData):
        errors = {}
        users = User.objects.filter(email=postData['email'])
        if users:
            errors['existing_user'] = 'Account with email already exists.'
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']=("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name requires at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name requires at least 2 characters.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password requires at least 8 characters.'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password']='Password must match.'
        return errors
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def login_validator(self, postData):
        errors = {}
        users = User.objects.filter(email=postData['email'])
        if not users.exists():
            errors['email'] = 'Email not found.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password requires at least 8 characters.'
        return errors

    def edit_validator(self, postData, logged_user_id):
        errors = {}
        users = User.objects.filter(email=postData['email'])
        if users.exists() and users[0].id != logged_user_id:
            errors['email'] = 'Email is already in use.'
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name requires at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name requires at least 2 characters.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password requires at least 8 characters.'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Password must match.'
        return errors

class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)  # Explicitly define primary key
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
