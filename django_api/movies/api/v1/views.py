from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...models.film_work import FilmWork
from ...models.person_film_work import RoleChoice


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        display_values = [
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
        ]
        queryset = self.model.objects.annotate(genres=ArrayAgg('film_genres__name', distinct=True))

        for role_key, role_name in RoleChoice.choices:
            display_values.append(role_key + 's')
            queryset = queryset.annotate(**{role_key + 's': ArrayAgg('persons__full_name',
                                                                     filter=Q(
                                                                         persons__personfilmwork__role=role_key
                                                                     ),
                                                                     distinct=True
                                                                     )
                                            }
                                         )

        return queryset.values(*display_values)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return self.object
