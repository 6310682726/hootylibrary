from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random as rand

class CustomAccountManager(BaseUserManager):

    def create_user(self, username, email, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(user_id=user_id_gen(), username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Admin must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Admin must be assigned to is_superuser=True.')
        
        return self.create_user(username, email, password, **other_fields)
    
def user_id_gen():
    rand_id = hex(rand.randint(0, pow(16, 8)))
    while len(User.objects.filter(pk=rand_id)) != 0:
        rand_id = hex(rand.randint(0, pow(16, 8))) 
    return rand_id
        

class User(AbstractBaseUser, PermissionsMixin):

    user_id = models.TextField(primary_key=True, max_length=10, default="0")
    username = models.CharField(unique=True, max_length=32)
    email = models.EmailField(_('Email'), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=16, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=32, null=True, blank=True)
    bio = models.CharField(_('bio'), blank=True, max_length=300)
    social_link = models.TextField(null=True)
    donation_link = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to="profile_pic/" + str(username), null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.user_id + self.username

class Book(models.Model):

    book_id = models.TextField(primary_key=True)
    book_name = models.CharField(max_length=60,default='Untitled')
    description = models.CharField(max_length=120, blank=True)
    date_created = models.DateField(default=timezone.now)
    book_type = models.IntegerField(default=1)
    thumbnail = models.ImageField(upload_to="book/" + str(book_id))
    pdf_files = models.FileField(upload_to="book/" + str(book_id) + "/pdfs")

class Genre(models.Model):
    genre = models.CharField(primary_key=True, max_length=20)
    books = models.ManyToManyField(Book, blank=True)

class Writes(models.Model):
    writer_id = models.OneToOneField(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

class Favorites(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

class Reviews(models.Model):
    reviewer_id = models.OneToOneField(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.FloatField(default=3.0)

class Issues(models.Model):
    issuer_id = models.OneToOneField(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    msg = models.CharField(max_length=500)

class Reports(models.Model):
    reporter_id = models.OneToOneField(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    msg = models.CharField(max_length=100, blank=True)