from .models import Games
from django_filters import rest_framework as filters

class GamesListFilter(filters.FilterSet):
    class Meta:
        model = Games
        fields = [
            "name",
            "is_active"
        ]

    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    is_active = filters.BooleanFilter(field_name="is_active")