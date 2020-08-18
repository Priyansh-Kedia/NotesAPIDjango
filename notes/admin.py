from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Note, Account, PhoneOTP

class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ['date','updated']
    list_display = ('note','account','date','updated','slug')
    search_fields = ['note','date']

class AccountAdmin(UserAdmin):
    list_display = ('phone','username','is_admin')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone','otp','verified')
       

admin.site.register(Note, NoteAdmin) 
admin.site.register(Account, AccountAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)