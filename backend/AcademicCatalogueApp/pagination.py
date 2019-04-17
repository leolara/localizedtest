from rest_framework.pagination import PageNumberPagination

# This class is used to make page sizes configurable in the request
class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 800
