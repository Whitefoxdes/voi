from rest_framework import pagination

class GamesListPagination(pagination.PageNumberPagination):

    page_size = 6
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 50