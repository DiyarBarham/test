from django.urls import path

from . import views
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('books', views.books),
    path('addbook', views.addbook),
    path('books/<int:id>', views.bookpage),
    path('editbook', views.editbook)
]