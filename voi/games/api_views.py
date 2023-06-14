from uuid import uuid4
from .models import Games
from .filter import GamesListFilter
from rest_framework import generics
from .serializer import GamesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from voi.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import GamesListPagination

class GamesSearchList(generics.ListAPIView):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GamesListFilter
    pagination_class = GamesListPagination
