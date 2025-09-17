from django.db import models
from datetime import date

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.name
    
    def get_trending_book(self):
        books = self.books.all()
        if not books.exists():
            return None

        def calculate_score(book):
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

        # pick book with highest trend score
        trending = max(books, key=calculate_score)
        return trending

    def update_image(self):
        trending_book = self.get_trending_book()
        if trending_book and trending_book.cover_image:
            self.image = trending_book.cover_image
            self.save()
    
class Book(models.Model):
    title = models.CharField(max_length=225)
    subtitle = models.CharField(max_length=250)
    cover_image = models.ImageField(upload_to="books/covers/", blank=True, null=True)
    author = models.CharField(max_length=225)
    isbn = models.CharField(max_length=13 , unique=True)
    category = models.ManyToManyField(Category, blank=True, related_name='books')
    description = models.TextField(blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    read_count = models.PositiveIntegerField(default=0)  # how many times borrowed/read
    published_at = models.DateField(null=True, blank=True)  # for recency

    def average_rating(self):
        ratings = self.reviews.all().values_list("rating", flat=True)
        return round(sum(ratings) / len(ratings), 1) if ratings else 0

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = sum(r.rating for r in reviews) / reviews.count()
        else:
            self.rating = 0
        self.save()
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
class Borrower(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class BorrowRecord(models.Model):
    class Status(models.TextChoices):
        BORROWED = "BORROWED", "Borrowed"
        RETURNED = "RETURNED", "Returned"
        OVERDUE = "OVERDUE", "Overdue"

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BORROWED)

    def __str__(self):
        return f"{self.book.title} ({self.status})"

class Fine(models.Model):
    borrow_record = models.OneToOneField(BorrowRecord, on_delete=models.CASCADE, related_name="fine")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine {self.amount:.2f} for {self.borrow_record}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    # user = models.ForeignKey(User, on_delete=models.CASCADE) we will add this part after authentication
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating})"

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # address = models.TextField(blank=True, null=True)
    # joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    