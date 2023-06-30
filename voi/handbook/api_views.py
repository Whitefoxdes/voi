from .models import (
    Handbook,
    HandbookType,
    HandbookScreenshot
    )


from uuid import uuid4
from user.models import User
from games.models import Games
from .serializer import (
    HandbookSerializer,
    HandbookTypeSerializer,
    HandbookScreeonshotSerializer
    )
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
    )
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from voi.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

class CreateHandbook(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, game_id):
        user_id = request.user.id

        serializer = HandbookSerializer(data=request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(
                {
                    "error_field_empty": "Request field empty"
                },
                status=400
            )

        data = serializer.data
        handbook_type = HandbookType.objects.filter(pk=data.get("type").get("id")).first()

        if not handbook_type:
            return Response(
                {
                    "error_handbook_type_not_allowed": "Handbook type not allowed",
                },
                status=400
            )
        
        user = User.objects.filter(pk=user_id).first()
        game = Games.objects.filter(pk=game_id).first()

        if not game:
            return Response(
                {
                    "error_game_not_found": "Game not found",
                },
                status=404
            )

        new_handbook = Handbook(
            title = data.get("title"),
            body = data.get("body"),
            author = user,
            game = game,
            type = handbook_type
        )

        new_handbook.save()

        return Response(
            {
                "status": "Create",
                "handbook_id" : new_handbook.id
            },
            status=200
        )

class ScreenshotUpload(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, handbook_id):
        serializer = HandbookScreeonshotSerializer(data=request.FILES)
        serializer.is_valid()
        if serializer.errors:
            return Response(
                {
                    "error_field_empty": "Request field empty"
                }, 
                status=400
            )
        
        data = serializer.validated_data
        handbook = Handbook.objects.filter(pk = handbook_id).first()

        if not handbook:
            return Response(
                {
                    "error_handbook_not_found": "Handbook not found"
                },
                status=404
            )
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
            
            screenshot_list.append(HandbookScreenshot(
                file_url=screenshot,
                handbook=handbook
                )
            )

        HandbookScreenshot.objects.bulk_create(screenshot_list)

        return Response({"status": "Upload"}, status=200)

class HandbookTypeList(generics.ListAPIView):
    queryset = HandbookType.objects.all()
    serializer_class = HandbookTypeSerializer
