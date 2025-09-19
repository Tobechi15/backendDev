from .serializers import *
from ..models import *
from ..utils.trending_books import *
from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response



class CategoryAPI(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related('books').all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all().prefetch_related('category')
    filterset_fields = ['categories__slug','author']
    search_fields = ['title','author','isbn','description']
    ordering_fields = ['published_date','total_reads','average_rating']

    def get_serializer_class(self):
        if self.action in ('create','update','partial_update'):
            return BookCreateUpdateSerializer
        return BookSerializer

    @action(detail=True, methods=['post'])
    def start_read():
        pass

    @action(detail=True, methods=['post'])
    def end_read():
        pass

    @action(detail=True, methods=['get'])
    def trending_books():
        top_books = get_top_trending_books(limit=5)
        return Response(top_books)

class TrendingBooksAPIView(generics.ListAPIView):
    queryset = Book.objects.all().order_by("-read_count", "-rating", "-published_at")[:3]
    serializer_class = BookSerializer

class TopAuthorsAPIView(APIView):
    def get(self, request):
        authors = (
            Book.objects.values("author").annotate(
                books_count=Count("id"),
                avg_rating=Avg("rating"),
                total_read=Count("read_count")
            ).order_by("-books_count", "-avg_rating")[:3]
        )
        return Response(authors)

class BorrowerViewSet(viewsets.ModelViewSet):

    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

