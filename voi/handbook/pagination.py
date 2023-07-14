from rest_framework import pagination

class HandbookListPagination(pagination.PageNumberPagination):

    page_size = 10
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 50