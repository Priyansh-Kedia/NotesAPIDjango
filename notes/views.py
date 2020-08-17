from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404

from random import randint

from .models import Note, Account, PhoneOTP
from .serializers import NotesSerializer, UserSerializer, AccountSerializer, PhoneOTPSerializer


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
        phoneOTP = None
        try:
            phoneOTP = PhoneOTP.objects.get(phone=request.POST.get('phone'))
        except PhoneOTP.DoesNotExist:
            pass

        if phoneOTP:
            if  not phoneOTP.verified:
                return Response({'error':'Please verify the phone number. OTP sent'})
            else:
                accountSerializer = AccountSerializer(data=request.data)
                data = {}
                if accountSerializer.is_valid():
                    accountSerializer.save()
                    data['success'] = 'Account created succesfully'
                    phoneOTP.delete()
                    return Response(data=data)
                else:
                    data['error'] = accountSerializer.errors
                    return Response(data)
        else:
            return Response({'error':'Please verify the phone number.'})

       

@api_view(['POST',])
def registerPhone(request):
    if request.method == 'POST':
        account = None
        try:
            account = Account.objects.get(phone=request.POST.get('phone'))
        except Account.DoesNotExist:
            pass
        if account:
            return Response({'error':'You have already registered'})
        else:
            phoneOTP = None
            try:
                phoneOTP = PhoneOTP.objects.get(phone=request.POST.get('phone'))
            except PhoneOTP.DoesNotExist:
                pass

            if phoneOTP and not phoneOTP.verified:
                return Response({'error':'OTP already sent. Please verify'})
            elif phoneOTP and phoneOTP.verified:
                return Response({'error':'Number already verified, please register'})
            else:
                otp = randint(100000,999999)
                PhoneOTP.objects.create(phone=request.POST.get('phone'), timestamp=timezone.now(), otp=otp)
                return Response({'otp':otp})


@api_view(['POST',])
def verifyPhone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        phoneOTP = None
        try:
            phoneOTP = PhoneOTP.objects.get(phone=phone)
        except PhoneOTP.DoesNotExist:
            pass

        if phoneOTP:
            if otp == str(phoneOTP.otp):
                phoneOTP.verified = True
                phoneOTP.save()
                return Response({'success':'OTP verified'})
            else:
                return Response({'error':'OTP not correct'})
        else:
            return Response({'error':'Phone number does not exist'})