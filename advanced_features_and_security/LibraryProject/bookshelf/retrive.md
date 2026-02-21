from bookshelf.models import Book
book = Book.objects.get(id=1)
print(book.title, book.author, book.publication_year)