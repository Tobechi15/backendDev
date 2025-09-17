from .serializers import *
from ..models import *
from rest_framework import viewsets


class CategoryAPI(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
