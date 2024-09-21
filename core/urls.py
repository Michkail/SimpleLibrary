"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, borrowed_books
from library.views import (BookListView, StudentBorrowedBooksView, borrow_book, renew_book,
                           LibrarianBookManagementView, return_book, LibrarianBorrowedBooksView)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Template views
    path('', index, name='index'),
    path('borrowed/', borrowed_books, name='borrowed_books'),

    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # API endpoints
    path('books/', BookListView.as_view(), name='book-list'),
    path('student/borrow/<int:book_id>/', borrow_book, name='borrow-book'),
    path('student/borrowed_books/', StudentBorrowedBooksView.as_view(), name='student-borrowed-books'),
    path('student/borrowed_books/renew/<int:pk>/', renew_book, name='renew-book'),
    path('librarian/manage_books/', LibrarianBookManagementView.as_view(), name='librarian-manage-books'),
    path('librarian/manage_books/return/<int:pk>/', return_book, name='return-book'),
    path('librarian/borrowed_books/', LibrarianBorrowedBooksView.as_view(), name='librarian-borrowed-books')
]
