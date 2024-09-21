from django.contrib import admin
from .models import (Genre, Filmwork, GenreFilmwork,
                     Person, PersonFilmwork)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',
                    'created', 'modified')
    search_fields = ('title', 'description', 'id')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',
                    'created', 'modified')
    search_fields = ('name', 'description', 'id')


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'type',
                    'creation_date', 'rating',
                    'created', 'modified')
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')


@admin.register(PersonFilmwork)
class PersonFilmworkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'genre', 'created')
    list_filter = ('film_work', 'genre',)
    search_fields = ('film_work', 'genre', 'id')


@admin.register(GenreFilmwork)
class GenreFilmworkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'genre', 'created')
    list_filter = ('film_work', 'genre',)
    search_fields = ('film_work', 'genre', 'id')
