from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, LogoutView

from .models import Book
from .models import Library
from .models import UserProfile

@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect('list_books')
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

def register_view(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user, role='Member')
        login(request, user)
        return redirect('list_books')
    return render(request, 'relationship_app/register.html', {'form': form})

@permission_required('relationship_app.can_add_book')
def add_book(request):
    return HttpResponse("Add book page (restricted by permission)")

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    return HttpResponse(f"Edit book page for book ID {book_id} (restricted by permission)")

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    return HttpResponse(f"Delete book page for book ID {book_id} (restricted by permission)")

def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
