from django.urls import include, path
from . import views

app_name = "book_views"
urlpatterns = [
    path('create_book', views.create_book, name='create_book'),
    path('pdf/<str:book_id>', views.book_pdf, name='book_pdf'),
    path('thumbnail/<str:book_id>/',views.book_thumbnail, name='book_thumbnail'),
    path('<str:book_id>/', views.book_views, name='book'),
    path('<str:book_id>/', include('messaging.urls')),
    
]