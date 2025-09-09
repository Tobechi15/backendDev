from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=225)
    subtitle = models.CharField(max_length=250)
    cover_image = models.ImageField(upload_to="books/covers/", blank=True, null=True)
    author = models.CharField(max_length=225)
    isbn = models.CharField(max_length=13 , unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    description = models.TextField(blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    def average_rating(self):
        ratings = self.reviews.all().values_list("rating", flat=True)
        return round(sum(ratings) / len(ratings), 1) if ratings else 0
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    # user = models.ForeignKey(User, on_delete=models.CASCADE) we will add this part after authentication
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
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

    