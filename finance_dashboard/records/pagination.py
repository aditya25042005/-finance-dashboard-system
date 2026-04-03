from rest_framework.pagination import PageNumberPagination


##we can make error handling better by creating custom exception handler 
class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    max_page_size = 10
