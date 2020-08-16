from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

from .utils import unique_slug_generator

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True, unique=False)
    phoneNumber = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.phoneNumber)


class Note(models.Model):
    note = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, related_name='author', on_delete=models.CASCADE)
    slug = models.SlugField(null=True,blank=True)

    class Meta:
        verbose_name = 'note'


def pre_save_note(sender,instance,*args,**kwargs):
    print('saving')
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()

pre_save.connect(pre_save_note, sender=Note)