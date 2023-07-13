from .models import (
    Handbook,
    HandbookType
)
from games.models import Games
from django_filters import rest_framework as filters

class HandbookListFilter(filters.FilterSet):
    class Meta:
        model = Handbook
        fields = [
            "game",
            "type"
        ]

    game = filters.ModelMultipleChoiceFilter(
        field_name='game',
        to_field_name='id',
        queryset=Games.objects.all()
    ),
    type = filters.ModelMultipleChoiceFilter(
        field_name='type',
        to_field_name='id',
        queryset=HandbookType.objects.all()
    )