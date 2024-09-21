from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


@login_required
def borrowed_books(request):
    return render(request, 'borrowed_books.html')
