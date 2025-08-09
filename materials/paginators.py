from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5  # Кол-во элементов по умолчанию
    page_size_query_param = "page_size"  # Позволяет переопределить через ?page_size=
    max_page_size = 20  # Максимум, что разрешено на одной странице
