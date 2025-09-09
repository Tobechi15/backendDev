from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('category/', views.books_by_category, name='category'),
    path('categories/', views.category_books, name='category_books'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    # path('books_by_author/', views.books_by_author, name='books_by_author'),
    path("books/author/<str:author>/", views.books_by_author, name="books_by_author"),
    path("books/<str:author>/<str:category>/", views.books_by_author_category, name="books_by_author_category"),
]