from rest_framework.pagination import PageNumberPagination

class Watchpages(PageNumberPagination):
    page_size = 4
    