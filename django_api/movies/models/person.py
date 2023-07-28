from django.db import models
from django.utils.translation import gettext_lazy as _

from .mix_in import UUIDMixin, TimeStampedMixin


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField()

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name
