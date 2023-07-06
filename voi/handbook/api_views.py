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
    HandbookScreenshotSerializer
    )
from rest_framework import generics
from .filter import HandbookListFilter
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
    )
from rest_framework.response import Response
from .pagination import HandbookListPagination
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
    permission_classes = [IsAuthenticated]
    
    def post(self, request, handbook_id):
        serializer = HandbookScreenshotSerializer(data=request.FILES)
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

class AllHandbookList(generics.ListAPIView):
    queryset = Handbook.objects.filter(
        is_active=True,
        is_delete=False
    ).all()
    serializer_class = HandbookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HandbookListFilter
    pagination_class=HandbookListPagination

class HandbookInfo(APIView):
    def get(self, request, handbook_id):
        handbook = Handbook.objects.filter(pk=handbook_id, is_delete=False).first()
        
        if not handbook:
            return Response(
                {
                    "error_handbook_not_found": "Not found"
                },
                status=404
            )

        serializer = HandbookSerializer(handbook)
        return Response({"handbook": serializer.data}, status=200)
    
class EditHandbook(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, handbook_id):
        
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

        handbook = Handbook.objects.filter(pk=handbook_id, is_delete=False).first()

        if not handbook:
            return Response(
                {
                    "error_handbook_not_found": "Handbook not found"
                },
                status=404
            )
        
        if user_id != handbook.author.id:
            return Response(
                {
                    "error_user_id": "Request data isn't yours"
                },
                status=403
            )

        handbook_type = HandbookType.objects.filter(pk=data.get("type").get("id")).first()

        if not handbook_type:
            return Response(
                {
                    "error_handbook_type_not_allowed": "Handbook type not allowed",
                },
                status=400
            )
        
        handbook.title = data.get("title")
        handbook.body = data.get("body")
        handbook.type = handbook_type
        handbook.is_active = False

        handbook.save()
        
        return Response(
            {
                "status": "Update"
            },
            status=200
        )
    
class DeleteHandbook(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, handbook_id):
        
        user_id = request.user.id

        handbook = Handbook.objects.filter(pk=handbook_id, is_delete=False).first()

        if not handbook:
            return Response(
                {
                    "error_handbook_not_found": "Handbook not found"
                },
                status=404
            )
    
        if user_id != handbook.author.id:
            return Response(
                {
                    "error_user_id": "Request data isn't yours"
                },
                status=403
            )
        
        handbook.is_delete = True

        handbook.save()

        return Response(
            {
                "status": "Delete"
            },
            status=200
        )

class DeleteScreenshot(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, handbook_id):
        
        old_screenshot_serializer = HandbookScreenshotSerializer(data=request.data)
        
        old_screenshot_serializer.is_valid()
        
        old_screenshot_data = old_screenshot_serializer.data

        if not old_screenshot_data.get("id"):
            return Response(
                {
                    "error_field_empty":"Request field empty"
                },
                status=400
            )

        old_screenshot_list = []

        for screenshot_id in old_screenshot_data.get("id"):
            if not HandbookScreenshot.objects.filter(pk=screenshot_id).exists():
                return Response(
                    {
                        "error_screenshot_not_found":"Screenshot not found"
                    },
                    status=400
                )
            old_screenshot = HandbookScreenshot.objects.filter(pk=screenshot_id, is_delete=False).first()

            if not old_screenshot:
                return Response(
                    {
                        "error_screenshot_already_delete":"Screenshot already delete"
                    },
                    status=400
                )

            old_screenshot.is_delete = True
            old_screenshot_list.append(old_screenshot)

        HandbookScreenshot.objects.bulk_update(
            old_screenshot_list,
            ["is_delete"]
        )

        return Response(
            {
                "status": "Delete"
            },
            status=200
        ) 