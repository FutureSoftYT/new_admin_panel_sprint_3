from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .genre import Genre
from .mix_in import UUIDMixin, TimeStampedMixin
from .person import Person


class FilmWork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        movie = 'movie', _('Movie')
        tv_show = 'tv_show', _('Tv Show')

    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), null=True, blank=True)
    rating = models.FloatField(_('rating'),
                               blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=255, choices=Type.choices)
    film_genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')

        indexes = [
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
            models.Index(fields=['rating'], name='film_work_rating_idx'),
        ]

    def __str__(self):
        return self.title
