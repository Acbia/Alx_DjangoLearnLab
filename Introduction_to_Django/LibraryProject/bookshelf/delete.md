```python
from bookshelf.models import Book

# Get the book and delete it
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify deletion
Book.objects.all()
```
