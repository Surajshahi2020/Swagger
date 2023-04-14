from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from typing import OrderedDict
from rest_framework.renderers import JSONRenderer
from rest_framework.compat import (
    INDENT_SEPARATORS,
    LONG_SEPARATORS,
    SHORT_SEPARATORS,
)
import json


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "page"
    page_size_query_param = "limit"
