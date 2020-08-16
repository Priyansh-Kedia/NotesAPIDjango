from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

from .models import Note, Author
from .serializers import NotesSerializer, UserSerializer


@api_view(['GET',])
def notes(request):
    notes = Note.objects.all()
    noteSerializer = NotesSerializer(notes,many=True)
    return Response(data=noteSerializer.data)

@api_view(['POST',])
def addNote(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            return Response({"error": "Not authenticated"})
        author = Author.objects.get(user=request.user)  
        data = {
            'author': {
                'phoneNumber': author.pk
            },
            'note': request.POST.get('note'),
            'date': timezone.now(),
            'updated': timezone.now()
        }
        noteSerializer = NotesSerializer(data=data)
        data = {}
        if noteSerializer.is_valid():
            note = noteSerializer.save()
            data['note'] = note.note
            data['success'] = "Note succesfully created"
        else:
            data = noteSerializer.errors
        return Response(data)


@api_view(['POST',])
def addNewUser(request):
    if request.method == 'POST':
        userSerializer = UserSerializer(data=request.data)
        data = {}
        if userSerializer.is_valid():
            user = userSerializer.save()
            data['username'] = user.first_name
            return Response(data)
        else:
            data = userSerializer.errors
            return Response(data)
