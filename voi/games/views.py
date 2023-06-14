from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class GamesSearchListView(APIView):
    def get(self, request):
        return render(request, "games_search.html")
