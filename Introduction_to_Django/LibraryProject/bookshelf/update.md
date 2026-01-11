```python
from bookshelf.models import Book

# Get the book and update the title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
Book.objects.get(id=book.id)
# Output: <Book: Nineteen Eighty-Four by George Orwell (1949)>
```
