from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404

from random import randint
import requests

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
            return Response(data, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT',])
def update_note(request,slug):
    if request.method == 'PUT':
        if request.user.is_anonymous:
            return Response({"error": "Not authenticated"},status=status.HTTP_401_UNAUTHORIZED)
        note = get_object_or_404(Note, slug=slug)
        user = request.user    
        account = Account.objects.get(phone=user.phone)
        if note:
            if note.account == account:
                note.note = request.POST.get('note')
                note.save()
                return Response({'success':'updated'},status=status.HTTP_200_OK)
            else:
                return Response({'error':'You are not authorized to edit this note'},status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['DELETE',])
def delete_note(request, slug):
    if request.method == 'DELETE':
        if request.user.is_anonymous:
            return Response({"error": "Not authenticated"},status=status.HTTP_401_UNAUTHORIZED)
        note = get_object_or_404(Note, slug=slug)
        user = request.user    
        account = Account.objects.get(phone=user.phone)
        if note:
            if note.account == account:
                task = note.delete()
                if task:
                    return Response({'success':'deleted'},status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'A problem occured'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'You are not authorized to edit this note'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST',])
def addNewNote(request):
    if request.method == "POST":
        if request.user.is_anonymous:
            return Response({'error':'Authetincation credentials not provided'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            account = get_object_or_404(Account, phone=request.user.phone)
            note = Note(account = account)
            noteSerializer = NotesSerializer(note,request.data)
            if noteSerializer.is_valid():
                noteSerializer.save()
                return Response({'success':'note saved succesfully'},status=status.HTTP_200_OK)
            else:
                return Response(noteSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({'user':request.user.phone},status=status.HTTP_201_CREATED)

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
                return Response({'error':'Please verify the phone number. OTP sent'},status=status.HTTP_400_BAD_REQUEST)
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
                    return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error':'Please verify the phone number.'},status=status.HTTP_400_BAD_REQUEST)

       

@api_view(['POST',])
def registerPhone(request):
    if request.method == 'POST':
        account = None
        phoneOTPSerializer = PhoneOTPSerializer(data=request.data)
        try:
            account = Account.objects.get(phone=request.POST.get('phone'))
        except Account.DoesNotExist:
            pass
        if account:
            return Response({'error':'You have already registered'},status=status.HTTP_400_BAD_REQUEST)
        else:
            phoneOTP = None
            try:
                phoneOTP = PhoneOTP.objects.get(phone=request.POST.get('phone'))
            except PhoneOTP.DoesNotExist:
                pass

            if phoneOTP and not phoneOTP.verified:
                return Response({'error':'OTP already sent. Please verify'},status=status.HTTP_400_BAD_REQUEST)
            elif phoneOTP and phoneOTP.verified:
                return Response({'error':'Number already verified, please register'},status=status.HTTP_400_BAD_REQUEST)
            else:
                otp = randint(100000,999999)
                if not phoneOTPSerializer.is_valid():
                    print(phoneOTPSerializer.errors)
                    return Response({'error':'The entered phone number is not of 10 digits'},status=status.HTTP_400_BAD_REQUEST)
                PhoneOTP.objects.create(phone=request.POST.get('phone'), timestamp=timezone.now(), otp=otp)
                response = url = "https://2factor.in/API/V1/{api_key}/SMS/+91{phone_no}/{custom_otp_val}".format(api_key="3fbfd8c1-e0b5-11ea-9fa5-0200cd936042",phone_no=request.POST.get('phone'),custom_otp_val=otp)
                print(response)
                requests.request("GET", url)
                return Response({'otp':otp},status=status.HTTP_200_OK)


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
                return Response({'success':'OTP verified'},status=status.HTTP_200_OK)
            else:
                return Response({'error':'OTP not correct'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'Phone number does not exist'},status=status.HTTP_400_BAD_REQUEST)