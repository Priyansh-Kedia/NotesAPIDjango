from django.contrib import admin

from .models import Note,Author

class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ['date','updated']

admin.site.register(Author)
admin.site.register(Note, NoteAdmin) 