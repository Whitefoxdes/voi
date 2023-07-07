from .models import Games, GameGenere
from django_filters import rest_framework as filters

class GamesListFilter(filters.FilterSet):
    class Meta:
        model = Games
        fields = [
            "name",
            "genere",
            "is_active"
        ]

    name = filters.CharFilter(field_name="name", lookup_expr="contains")
    genere = filters.ModelMultipleChoiceFilter(
        field_name='genere',
        to_field_name='id',
        queryset=GameGenere.objects.all()
    )