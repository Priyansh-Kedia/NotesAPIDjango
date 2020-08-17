from django.urls import path
from . import views

urlpatterns = [
    path('',views.notes),
    path('add',views.addNewNote),
    path('user/account',views.addAccount),
    path('get/<slug:slug>/',views.get_note_by_slug),
    path('update/<slug:slug>', views.update_note),
    path('delete/<slug:slug>/',views.delete_note)
]