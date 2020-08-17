from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MaxLengthValidator, int_list_validator, MinLengthValidator

from .utils import unique_slug_generator



class AccountManager(BaseUserManager):
    def create_user(self, phone,username, password=None):
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone = phone,
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone,username,password):
        user = self.create_user(
           phone = phone,
           password=password,
           username = username, 
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    phone = models.IntegerField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_login = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username',]

    objects = AccountManager()

    def __str__(self):
        return str(self.phone)

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

class Note(models.Model):
    note = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(Account, related_name='account', on_delete=models.CASCADE, null=True)
    slug = models.SlugField(null=True,blank=True)

    class Meta:
        verbose_name = 'note'

    def __str__(self):
        return self.note + str(self.account.phone)


def pre_save_note(sender,instance,*args,**kwargs):
    print('saving')
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()

pre_save.connect(pre_save_note, sender=Note)