from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models.film_work import FilmWork
from .models.genre import Genre
from .models.genre_film_work import GenreFilmWork
from .models.person import Person
from .models.person_film_work import PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    verbose_name_plural = _('genres film')


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    verbose_name_plural = _('persons film')


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

    raw_id_fields = ['persons', 'film_genres']

    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')
    list_filter = ('type', 'film_genres', 'creation_date')

    search_fields = ('title',)

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.film_genres.all()])

    def get_persons(self, obj):
        return ','.join([person.full_name for person in obj.persons.all()])

    get_genres.short_description = _('Genres')
    get_persons.short_description = _('Persons')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
