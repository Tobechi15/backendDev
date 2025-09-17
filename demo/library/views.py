from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import DetailView
from django.http import HttpResponse
from django.db.models import Count, Q, Sum
from collections import defaultdict
from .models import *
from .forms import *
from .utils.trending_books import *

# Create your views here.
def home(request):
    template_name = "home/index.html"
    books = Book.objects.all()
    category = Category.objects.all()
    top_books = get_top_trending_books(limit=5)
    most_read_books = Book.objects.order_by("-read_count")[:5]

    total_borrowed = BorrowRecord.objects.count()

    total_read = BorrowRecord.objects.count() # Number of books borrowed (all time)

    # total books per author
    top_authors = (
        Book.objects.values("author")
        .annotate(total_books=Count("id"))
        .order_by("-total_books")  # sort by popularity
    )

    recommended_categories = (
        Category.objects.annotate(total_reads=Sum("books__read_count"))
        .filter(total_reads__gt=0)  # exclude categories with no reads
        .order_by("-total_reads")[:5]
    )
    context = {
        "books": books,
        "category": category,
        "top_authors": top_authors,
        "recommended_categories": recommended_categories,
        "most_read_books": most_read_books,
        "total_borrowed": total_borrowed,
        "total_read": total_read,
    }
    return render(request, template_name, context)


def search(request):
    query = request.GET.get("q", "").strip()
    book_results = []
    category_results = []

    if query:
        # Search in books (title, subtitle, author, description, isbn)
        book_results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(subtitle__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct()

        # Search in categories (name, description)
        category_results = Category.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    context = {
        "query": query,
        "book_results": book_results,
        "category_results": category_results,
    }
    return render(request, "components/search_result.html", context)

def book(request):
    model = book
    template_name = "book/book.html"
    books = Book.objects.all()

    return render(request, template_name, {"books": books})

class BookDetailView(DetailView):
    model = Book
    template_name = "book/book_detail.html"
    context_object_name = "book"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment reads only when user GETs the page, not on form POST
        if self.request.method == "GET":
            obj.reads = obj.read_count + 1
            obj.save(update_fields=["read_count"])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = self.object
            review.user = request.user
            review.save()
            self.object.rating()
        return redirect("book_detail", pk=self.object.pk)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("book")) # To redirect to the books page after adding a book
        else:
            return render(request, "book/add_book.html", {"form":form})
    else:
        form = BookForm(request.POST)
    return render(request, "book/add_book.html", {"form":form})

def available_books(request):
    books = Book.objects.filter(is_available=True)
    return render(request, "book/available_books.html", {"books": books})

# def show_cat(request):
#     model = book
#     template_name = "categories.html"
#     books = Book.objects.all()
#     category = Category.objects.all()

#     return render(request, template_name, {"books": books, "category":category})

def show_books():
    pass

def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book')
    else:
        return render(request, "add_book.html", {"form": BookForm(instance=book)})

def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)
    return render(request, "book/categories.html", {
        "category": category,
        "books": books
    })    

def category_sections(request):
    categories = Category.objects.prefetch_related("books").all()
    return render(request, "book/category_sections.html", {
        "categories": categories
    })

def books_by_category(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "book/categories.html", context=context)


# def books_by_author(request):
#     books = Book.objects.select_related("category").all().order_by("author", "category__name")

#     authors_data = defaultdict(lambda: defaultdict(list))
#     for book in books:
#         authors_data[book.author][book.category.name].append(book)

#     return render(request, "book/books_by_author.html", {"authors_data": dict(authors_data)})

def books_by_author_category(request, author, category):
    books = Book.objects.filter(author=author, category__name=category)
    return render(request, "book/author_category.html", {"books": books, "author": author, "category": category})

def books_by_author(request, author):
    books = Book.objects.filter(author=author).select_related("category")
    return render(request, "book/author_books.html", {"books": books, "author": author})

def borrow_book(request):
    if request.method == "POST":
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data["member_id"]
            book_id = form.cleaned_data["book_id"]

            member = get_object_or_404(Member, id=member_id)
            book = get_object_or_404(Book, id=book_id, is_available=True)

            BorrowRecord.objects.create(member=member, book=book)
            book.is_available = False
            book.save()

            messages.success(request, f"{member.name} borrowed {book.title}.")
            return redirect("library:available_books")
    else:
        form = BorrowBookForm()

    return render(request, "book/borrow_book.html", {"form": form})

def return_book(request):
    if request.method == "POST":
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            record_id = form.cleaned_data["record_id"]
            record = get_object_or_404(BorrowRecord, id=record_id, returned_on__isnull=True)

            record.returned_on = record.returned_on or record.borrowed_on
            record.book.is_available = True
            record.book.save()
            record.save()

            messages.success(request, f"{record.book.title} has been returned.")
            return redirect("library:available_books")
    else:
        form = ReturnBookForm()

    return render(request, "book/return_book.html", {"form": form})
