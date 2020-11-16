from rest_framework.pagination import PageNumberPagination

class CommentPagination(PageNumberPagination):
    page_size = 5

class SongPagination(PageNumberPagination):
    page_size = 20