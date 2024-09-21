from rest_framework import generics
from .models import Book, BorrowedBook, Student
from .serializers import BookSerializer, BorrowedBookSerializer, StudentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone


# List all books, available for anyone
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


# For students to see borrowed books and renew them
class StudentBorrowedBooksView(generics.ListAPIView):
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)

        return BorrowedBook.objects.filter(student=student)


class LibrarianBorrowedBooksView(generics.ListAPIView):
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowedBook.objects.all()


# For students to borrow a book
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request, book_id):
    try:
        student = Student.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)

        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()

            borrowed_book = BorrowedBook.objects.create(book=book,
                                                        student=student,
                                                        borrow_date=timezone.now(),
                                                        return_date=timezone.now() + timezone.timedelta(days=30),
                                                        is_renewed=False)

            return Response({'message': 'Book borrowed successfully',
                             'borrowed_book': BorrowedBookSerializer(borrowed_book).data})

        else:
            return Response({'message': 'No available copies'}, status=400)

    except Book.DoesNotExist:
        return Response({'message': 'Book not found'}, status=404)

    except Student.DoesNotExist:
        return Response({'message': 'Student not found'}, status=404)


# For students to renew a book
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def renew_book(request, pk):
    try:
        borrowed_book = BorrowedBook.objects.get(id=pk, student__user=request.user)

        if not borrowed_book.is_renewed:
            borrowed_book.return_date += timezone.timedelta(days=30)
            borrowed_book.is_renewed = True
            borrowed_book.save()

            return Response({'message': 'Book renewed successfully'})

        else:
            return Response({'message': 'Book has already been renewed'}, status=400)

    except BorrowedBook.DoesNotExist:
        return Response({'message': 'Borrowed book not found'}, status=404)


# For librarian to manage borrow/return
class LibrarianBookManagementView(generics.ListCreateAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request, pk):
    try:
        borrowed_book = BorrowedBook.objects.get(id=pk)
        borrowed_book.book.available_copies += 1
        borrowed_book.book.save()
        borrowed_book.delete()

        return Response({'message': 'Book returned successfully'})

    except BorrowedBook.DoesNotExist:
        return Response({'message': 'Borrowed book not found'}, status=404)
