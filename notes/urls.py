from django.urls import path
from . import views

urlpatterns = [
    path('',views.notes),
    path('phone',views.registerPhone),
    path('phone/verify',views.verifyPhone),
    path('add',views.addNewNote),
    path('user/account',views.addAccount),
    path('get/<slug:slug>/',views.get_note_by_slug),
    path('update/<slug:slug>', views.update_note),
    path('delete/<slug:slug>/',views.delete_note)
]