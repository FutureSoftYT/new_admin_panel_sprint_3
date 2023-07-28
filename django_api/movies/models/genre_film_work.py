from django.db import models

from .mix_in import UUIDMixin


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"

        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='unique_film_genre'),
        ]

        indexes = [
            models.Index(fields=['film_work', 'genre'], name='film_work_genre_idx'),
        ]

    def __str__(self):
        return self.genre.name
