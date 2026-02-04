# Advanced API Project (DRF Generic Views)

This project extends the Django REST Framework setup with generic views for
CRUD operations on the `Book` model, including permissions and basic filtering.

## Endpoints

All API routes are prefixed with `/api/`.

- `GET /api/books/`
  - Lists all books (public).
  - Supports search and ordering:
    - `?search=earthsea`
    - `?ordering=publication_year` or `?ordering=-publication_year`
- `GET /api/books/<id>/`
  - Retrieves a single book by ID (public).
- `POST /api/books/create/`
  - Creates a new book (authenticated only).
- `PUT /api/books/<id>/update/`
  - Updates an existing book (authenticated only).
- `PATCH /api/books/<id>/update/`
  - Partially updates an existing book (authenticated only).
- `DELETE /api/books/<id>/delete/`
  - Deletes a book (authenticated only).

## Permissions

- Read-only endpoints (`list`, `detail`) allow unauthenticated access.
- Write endpoints (`create`, `update`, `delete`) require authentication.

## View Configuration Notes

- Views are implemented with DRF generic views in `api/views.py`.
- `BookListView` adds `SearchFilter` and `OrderingFilter` to demonstrate
  built-in DRF filtering.
- `BookCreateView` and `BookUpdateView` override `perform_create` and
  `perform_update` as extension hooks; serializer validation runs before save.

## Example Requests

List books:

```bash
curl http://127.0.0.1:8000/api/books/
```

Create a book (replace `<token>` with an auth token if using token auth):

```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"A Wizard of Earthsea\",\"publication_year\":1968,\"author\":1}"
```

Update a book:

```bash
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"The Tombs of Atuan\",\"publication_year\":1971,\"author\":1}"
```

Delete a book:

```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/
```
