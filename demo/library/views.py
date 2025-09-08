from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Book
from .models import Category
from .forms import BookForm

# Create your views here.
def home(request):
    model = book
    template_name = "index.html"
    books = Book.objects.all()
    return render(request, template_name, {"books": books})

def book(request):
    model = book
    template_name = "book.html"
    books = Book.objects.all()

    return render(request, template_name, {"books": books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "book.html", {"book": Book.objects.all()})
        else:
            return render(request, "add_book.html", {"form":form})
    else:
        form = BookForm(request.POST)
    return render(request, "add_book.html", {"form":form})


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
    

def books_by_category(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "categories.html", context=context)
