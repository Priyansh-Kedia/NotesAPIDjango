from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Note, Author
from .serializers import NotesSerializer, UserSerializer


@api_view(['GET',])
def notes(request):
    notes = Note.objects.all()
    noteSerializer = NotesSerializer(notes,many=True)
    return Response(data=noteSerializer.data)

@api_view(['GET',])
def get_note_by_slug(request,slug):
    if request.method == 'GET':
        note = None
        try:
            note = Note.objects.get(slug=slug)
            noteSerializer = NotesSerializer(note)
            return Response(noteSerializer.data)
        except Note.DoesNotExist:
            data = {'error':'No such note exists'}
            return Response(data)

@api_view(['PUT',])
def update_note(request,slug):
    if request.method == 'PUT':
        if request.user.is_anonymous:
            return Response({"error": "Not authenticated"})
        note = get_object_or_404(Note, slug=slug)
        user = request.user    
        author = Author.objects.get(user=user)
        if note:
            if note.author.user == user:
                note.note = request.POST.get('note')
                note.save()
                return Response({'success':'updated'})
            else:
                return Response({'error':'You are not authorized to edit this note'})
    

@api_view(['DELETE',])
def delete_note(request, slug):
    if request.method == 'DELETE':
        if request.user.is_anonymous:
            return Response({"error": "Not authenticated"})
        note = get_object_or_404(Note, slug=slug)
        user = request.user    
        author = Author.objects.get(user=user)
        if note:
            if note.author.user == user:
                task = note.delete()
                if task:
                    return Response({'success':'deleted'})
                else:
                    return Response({'error': 'A problem occured'})
            else:
                return Response({'error':'You are not authorized to edit this note'})


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

