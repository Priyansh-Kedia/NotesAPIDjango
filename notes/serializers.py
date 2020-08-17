from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Note, Account


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

class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'




