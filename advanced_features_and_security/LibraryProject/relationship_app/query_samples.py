import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def queries():
    
    author_name = "Chinua Achebe"
    author = Author.objects.get(name=author_name)
    print(f"Books by {author.name}:")
    for book in Book.objects.filter(author=author):
        print(book.title)

    
    library_name = "Main Library"
    library = Library.objects.get(name=library_name)
    print(f"\nBooks in {library.name}:")
    for book in library.books.all():
        print(book.title)

   
    librarian = Librarian.objects.get(library=library)
    print(f"\nLibrarian for {library.name}: {librarian.name}")

if __name__ == "__main__":
    queries()
