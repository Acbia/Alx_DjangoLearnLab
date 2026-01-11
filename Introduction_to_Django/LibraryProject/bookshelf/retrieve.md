```python
from bookshelf.models import Book

# Retrieve all books
books = Book.objects.all()
books
# Output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>

# Retrieve a single book
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
# Output: ('1984', 'George Orwell', 1949)

