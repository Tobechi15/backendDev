from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'category', CategoryAPI)
router.register(r'book', BookViewSet)
router.register(r'borrower', BorrowerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('trending-books/', TrendingBooksAPIView.as_view(), name='trending-books'),
    path('top-authors/', TopAuthorsAPIView.as_view(), name="top-authors"),
]


