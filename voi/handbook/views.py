from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class CreateHandbookView(APIView):
    def get(self, request, game_id):
        return render(request, "create_handbook.html")