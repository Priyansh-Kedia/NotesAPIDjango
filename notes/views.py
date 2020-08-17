from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Note, Author, Account
from .serializers import NotesSerializer, UserSerializer, AccountSerializer


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
        account = Account.objects.get(phone=user.phone)
        if note:
            if note.account == account:
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
        account = Account.objects.get(phone=user.phone)
        if note:
            if note.account == account:
                task = note.delete()
                if task:
                    return Response({'success':'deleted'})
                else:
                    return Response({'error': 'A problem occured'})
            else:
                return Response({'error':'You are not authorized to edit this note'})

@api_view(['POST',])
def addNewNote(request):
    if request.method == "POST":
        if request.user.is_anonymous:
            return Response({'error':'Authetincation credentials not provided'})
        else:
            account = get_object_or_404(Account, phone=request.user.phone)
            note = Note(account = account)
            noteSerializer = NotesSerializer(note,request.data)
            if noteSerializer.is_valid():
                noteSerializer.save()
                return Response({'success':'note saved succesfully'})
            else:
                return Response(noteSerializer.errors)
            return Response({'user':request.user.phone})

@api_view(['POST',])
def addAccount(request):
    print(request.data)
    if request.method == 'POST':
        accountSerializer = AccountSerializer(data=request.data)
        data = {}
        if accountSerializer.is_valid():
            accountSerializer.save()
            data['success'] = 'Account created succesfully'
        else:
            data['error'] = accountSerializer.errors
        return Response(data)