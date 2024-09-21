from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BorrowedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    is_renewed = models.BooleanField(default=False)
    history = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'{self.book.title} - {self.student.name}'


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
