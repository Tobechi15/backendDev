from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('category/', views.books_by_category, name='category'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit', views.edit_book, name='edit_book'),
]