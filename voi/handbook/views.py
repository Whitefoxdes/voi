from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class CreateHandbookView(APIView):
    def get(
            self,
            request, 
            game_id):

        return render(request, "create_handbook.html")

class AllHandbookListView(APIView):
    def get(
            self,
            request):

        return render(request, "all_handbook_list.html")

class HandbookInfoView(APIView):
    def get(
            self,
            request, 
            handbook_id):

        return render(request, "handbook_info.html")

class EditHandbookView(APIView):
    def get(
        self,
        request, 
        handbook_id):

        return render(request, "edit_handbook.html")