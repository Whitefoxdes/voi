from .models import Handbook
from games.models import Games
from django_filters import rest_framework as filters

class HandbookListFilter(filters.FilterSet):
    class Meta:
        model = Handbook
        fields = [
            "game",
            # "is_active"
        ]

    game = filters.ModelMultipleChoiceFilter(
        field_name='game',
        to_field_name='id',
        queryset=Games.objects.all()
    )
    # is_active = filters.BooleanFilter(field_name="is_active")