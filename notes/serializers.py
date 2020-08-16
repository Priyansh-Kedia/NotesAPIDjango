from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Note, Author

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['note',]

    # def save(self):
    #     note = Note (
    #         note=self.validated_data['note'],
    #         date = timezone.now(),
    #         updated= timezone.now(),
    #     )
    #     note.save()
    #     print(note.note)


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
