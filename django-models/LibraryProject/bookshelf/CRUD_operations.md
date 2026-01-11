CRUD Operations for Book Model
Create
from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()



Retrieve
from bookshelf.models import Book
book = Book.objects.get(id=1)
print(book.title, book.author, book.publication_year)



Update
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)



Delete
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.delete()
books = Book.objects.all()
print(books)

