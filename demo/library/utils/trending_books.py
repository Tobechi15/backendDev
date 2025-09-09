from datetime import date
from django.db.models import QuerySet
from ..models import Book

def calculate_trend_score(book):
    """Calculate trend score for a book based on rating, reads, and recency."""
    # rating weight
    rating_score = float(book.rating) * 2

    # read count weight
    read_score = book.read_count * 1.5

    # recency weight (newer = higher)
    recency_score = 0
    if book.published_at:
        days_old = (date.today() - book.published_at).days
        recency_score = max(0, 1000 - days_old) / 100  # recent books get up to +10

    return rating_score + read_score + recency_score

def get_top_trending_books(limit=5) -> QuerySet:
    books = Book.objects.all()
    if not books.exists():
        return Book.objects.none()

    # Annotate each book with its trend score
    scored_books = [(book, calculate_trend_score(book)) for book in books]
    scored_books.sort(key=lambda x: x[1], reverse=True)  # sort by score desc

    # Return top N
    return [book for book, score in scored_books[:limit]]

