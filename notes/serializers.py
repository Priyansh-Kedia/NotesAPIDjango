from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Note, Author, Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','username']

    def save(self):
        email = self.validated_data['email']
        if User.objects.filter(email=email):
            raise serializers.ValidationError('email already exists')
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email = self.validated_data['email'],
            password = self.validated_data['password'],
            username= self.validated_data['username']
        )

        user.save()
        return user

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone','username','password']

    def save(self):
        username = self.validated_data['username']

        account = Account(
            phone=self.validated_data['phone'],
            username = username,
            password = self.validated_data['password']
        )

        account.save()
        return account


class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ['id','phoneNumber',]


class NotesSerializer(serializers.ModelSerializer):
 #   author = AuthorSerializer()

    class Meta:
        model = Note
        fields = '__all__'

    # def save(self):
    #    # author = Author.objects.get(pk=self['author']['phoneNumber'].value)
    #     note = Note(
    #         note= self.validated_data['note'],
    #         date=self['date'],
    #         updated=self['updated']
    #     )
        
    #     note.save()
    #     return note




