from django.urls import path
from . import views

urlpatterns = [
    path('',views.notes),
    path('add',views.addNote),
    path('user/add',views.addNewUser),
    path('get/<slug:slug>/',views.get_note_by_slug),
    path('update/<slug:slug>', views.update_note),
    path('delete/<slug:slug>/',views.delete_note)
]