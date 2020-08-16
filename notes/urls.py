from django.urls import path
from . import views

urlpatterns = [
    path('',views.notes),
    path('add',views.addNote),
    path('user/add',views.addNewUser)
]