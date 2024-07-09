from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('feedback/', views.getFeedback, name='feedback'),
    path(r'findbooks', views.findbooks, name='findbooks'),
    path(r'place_order', views.place_order, name='place_order'),
    ]
