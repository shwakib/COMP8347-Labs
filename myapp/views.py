from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import Book
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm, OrderForm


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})


def about(request):
    # return render(request, 'myapp/about.html')
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/about.html', {'booklist': booklist})


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    ## passed the book object as book_details in the context and this varialbe contais details of the books
    return render(request, 'myapp/details.html', {'book_details': book})


# This will redirect to the /myapp path
def home(request):
    return redirect('myapp:about')


# def home(request):
#     return render(request, 'home.html')
#
#
# def about_us(request):
#     return render(request, 'about_us.html')

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else:
                choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})


def findbooks(request):
    if request.method == 'GET':
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price)

            context = {'name': name, 'booklist': booklist}
            return render(request, 'myapp/results.html', context)
        else:
            return render(request, 'myapp/findbooks.html', {'form': form, 'error': 'Invalid data'})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.status
            order.save()
            form.save_m2m()

            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            # return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
            return render(request, 'myapp/order_response.html',{'books': books, 'order': order, 'member': member, 'order_type': type})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})
