from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class GamesSearchListView(APIView):
    def get(
            self,
            request):

        return render(request, "games_search.html")

class AddNewGame(APIView):
    def get(
            self,
            request):

        return render(request, "add_new_game.html")

class AllGamesListView(APIView):
    def get(
            self,
            request):

        return render(request, "all_games.html")

class GameInfo(APIView):
    def get(
            self,
            request,
            game_id):

        return render(request, "game_info.html")