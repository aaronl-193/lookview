from django.contrib import admin

from .models import Film, FilmTag

admin.site.register(Film)
admin.site.register(FilmTag)
