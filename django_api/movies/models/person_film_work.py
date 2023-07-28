from django.db import models
from django.utils.translation import gettext_lazy as _

from .film_work import FilmWork
from .mix_in import UUIDMixin
from .person import Person


class RoleChoice(models.TextChoices):
    actor = 'actor', _('Actor')
    director = 'director', _('Director')
    writer = 'writer', _('Writer')


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255, choices=RoleChoice.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"

        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='unique_person_film_role'),
        ]

        indexes = [
            models.Index(fields=['film_work', 'person', 'role'], name='film_person_work_idx')
        ]

    def __str__(self):
        return self.role
