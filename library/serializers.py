from rest_framework import serializers
from library.models import Book, Student, BorrowedBook


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'total_copies', 'available_copies']


class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    student_name = serializers.CharField(source='student.user.username')

    class Meta:
        model = BorrowedBook
        fields = ['book', 'borrow_date', 'return_date', 'is_renewed', 'student_name']


class StudentSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowedBookSerializer(many=True)

    class Meta:
        model = Student
        fields = ['name', 'borrowed_books']


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['student', 'book', 'borrow_date', 'return_date']
