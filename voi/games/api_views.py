from uuid import uuid4
from .filter import GamesListFilter
from rest_framework import generics
from rest_framework.views import APIView
from .models import Games, GameScreenshot
from .pagination import GamesListPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from voi.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import GamesSerializer, GameScreeonshotSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class GamesSearchList(generics.ListAPIView):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GamesListFilter
    pagination_class = GamesListPagination

class AddGame(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        serializer = GamesSerializer(data=request.data)

        serializer.is_valid()
        if serializer.errors:
            return Response(
                {
                    "error_field_empty": "Request field empty"
                }, 
                status=400
            )

        data = serializer.validated_data
        if Games.objects.filter(name=data["name"]).exists():
            return Response(
                {
                    "error_game_exist":"Game exist"
                },
                status=400)
        
        new_game = Games(name = data.get("name"), is_active=True)
        new_game.save()

        return Response(
            {
                "status": "Created",
                "game_id": new_game.id
            },
            status=200
        )
    
class ScreenshotForGameUpload(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    def put(self, request, game_id):
        serializer = GameScreeonshotSerializer(data=request.FILES)
        serializer.is_valid()
        if serializer.errors:
            return Response(
                {
                    "error_field_empty": "Request field empty"
                }, 
                status=400
            )
        
        data = serializer.validated_data

        game = Games.objects.filter(pk = game_id).first()

        screenshot_list = []
        
        for screenshot in data.get("file_url"):
            if screenshot.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                return Response(
                    {
                        "error_file_size": "File size is too large"
                    },
                    status=400
                )
            
            file_ext = screenshot.name.split(".")[1]

            if file_ext not in ["png","jpg","jpeg","gif",]:
                return Response(
                    {
                        "error_file_ext": "Invalid file type"
                    },
                    status=400
                )
            
            screenshot_list.append(GameScreenshot(
                file_url=screenshot,
                game=game
                )
            )

        GameScreenshot.objects.bulk_create(screenshot_list)

        return Response({"status": "Upload"}, status=200)

class AllGamesList(generics.ListAPIView):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    pagination_class = GamesListPagination