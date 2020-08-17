from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Note, Account

class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ['date','updated']

class AccountAdmin(UserAdmin):
    list_display = ('phone','username','is_admin')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
       

admin.site.register(Note, NoteAdmin) 
admin.site.register(Account, AccountAdmin)