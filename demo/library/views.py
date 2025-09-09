from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.db.models import Count
from collections import defaultdict
from .models import Book
from .models import Category
from .forms import BookForm

# Create your views here.
def home(request):
    template_name = "home/index.html"
    books = Book.objects.all()
    category = Category.objects.all()

    # total books per author
    top_authors = (
        Book.objects.values("author")
        .annotate(total_books=Count("id"))
        .order_by("-total_books")  # sort by popularity
    )

    context = {
        "books": books,
        "category": category,
        "top_authors": top_authors,
    }
    return render(request, template_name, context)

def book(request):
    model = book
    template_name = "book/book.html"
    books = Book.objects.all()

    return render(request, template_name, {"books": books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, "library:book.html", {"book": Book.objects.all()}) # To redirect to the books page after adding a book
        else:
            return render(request, "book/add_book.html", {"form":form})
    else:
        form = BookForm(request.POST)
    return render(request, "book/add_book.html", {"form":form})


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

