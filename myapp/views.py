from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from myapp.models import Book, Review
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg
import random
from django.utils import timezone
from datetime import timedelta


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    last_login = request.session.get('last_login')
    if last_login:
        message = f"Your last login was on {last_login}."
    else:
        message = "Your last login was more than one hour ago."
    # return render(request, 'myapp/index.html', {'booklist': booklist})
    return render(request, 'myapp/index.html', {'booklist': booklist, 'message': message})


@login_required
def about(request):
    # return render(request, 'myapp/about.html')
    # booklist = Book.objects.all().order_by('id')[:10]
    # return render(request, 'myapp/about.html', {'booklist': booklist})
    if 'lucky_num' in request.COOKIES:
        mynum = request.COOKIES['lucky_num']
    else:
        mynum = random.randint(1, 100)

    response = render(request, 'myapp/about.html', {'booklist': Book.objects.all().order_by('id')[:10], 'mynum': mynum})

    # Set the cookie to expire in 5 minutes
    expire_time = timezone.now() + timedelta(minutes=1)
    response.set_cookie('lucky_num', mynum, expires=expire_time)

    return response


@login_required
def detail(request, book_id):
    user = request.user
    if hasattr(user, 'member'):
        book = get_object_or_404(Book, id=book_id)
        return render(request, 'myapp/details.html', {'book_details': book})
    else:
        message = "You are not a registered member!"
        return render(request, 'myapp/details.html', {'message': message})

    # passed the book object as book_details in the context and this variable contain details of the books



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
            choices = []
            if 'B' in feedback:
                choices.append('to borrow books')
            if 'P' in feedback:
                choices.append('to purchase books')
            choice = ','.join(choices) if choices else 'None'
            # if feedback == 'B':
            #     choice = ' to borrow books.'
            # elif feedback == 'P':
            #     choice = ' to purchase books.'
            # else:
            #     choice = ' None.'
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
            return render(request, 'myapp/order_response.html',
                          {'books': books, 'order': order, 'member': member, 'order_type': type})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save()
                book = review.book
                book.num_reviews += 1
                book.save()
                return redirect('myapp:index')
            else:
                form.add_error('rating', 'You must enter a rating between 1 and 5!')
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


def user_login(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(username=username, password=password)
    #     if user:
    #         if user.is_active:
    #             login(request, user)
    #             return HttpResponseRedirect(reverse('myapp:index'))
    #         else:
    #             return HttpResponse('Your account is disabled.')
    #     else:
    #         return HttpResponse('Invalid login details.')
    # else:
    #     return render(request, 'myapp/login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                last_login_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session['last_login'] = last_login_time
                request.session.set_expiry(3600)  # Session expiry set to 1 hour
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def chk_reviews(request, book_id):
    user = request.user
    if hasattr(user, 'member'):
        book = get_object_or_404(Book, id=book_id)
        avg_rating = Review.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
        if avg_rating is None:
            message = "No reviews have been submitted for this book."
        else:
            message = f"The average rating for this book is {avg_rating:.1f}."
        return render(request, 'myapp/chk_reviews.html', {'message': message, 'book': book})
    else:
        message = "You are not a registered member!"
        return render(request, 'myapp/chk_reviews.html', {'message': message})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))
