# Social Media API

This is a Django + Django REST Framework social media API with custom user authentication, posts, and comments.

## Tech Stack
- Python 3
- Django
- Django REST Framework
- DRF Token Authentication
- SQLite (default)

## Implemented Features
- New Django project: `social_media_api`
- App for account management: `accounts`
- App for post and comment management: `posts`
- Custom user model extending `AbstractUser` with:
  - `bio` (text)
  - `profile_picture` (URL)
  - `followers` (self-referential many-to-many, `symmetrical=False`)
- Token authentication via `rest_framework.authtoken`
- Authentication endpoints:
  - `POST /register`
  - `POST /login`
  - `GET /profile`
  - `PUT/PATCH /profile`
- Post endpoints (router):
  - `GET /api/posts/`
  - `POST /api/posts/`
  - `GET /api/posts/{id}/`
  - `PUT/PATCH /api/posts/{id}/`
  - `DELETE /api/posts/{id}/`
- Comment endpoints (router):
  - `GET /api/comments/`
  - `POST /api/comments/`
  - `GET /api/comments/{id}/`
  - `PUT/PATCH /api/comments/{id}/`
  - `DELETE /api/comments/{id}/`

Both `register` and `login` return an auth token on success.
Post/comment update and delete are restricted to the resource author.

## Setup Instructions
1. Install dependencies (if needed):

```bash
pip install django djangorestframework
```

2. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Run the development server:

```bash
python manage.py runserver
```

## Authentication
Use token auth in protected endpoints:

```http
Authorization: Token <your_token>
```

All `/api/posts/` and `/api/comments/` routes require authentication.

## API Usage

### 1) Register
`POST /register`

Request body example:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "strongpass123",
  "first_name": "Alice",
  "last_name": "Walker",
  "bio": "Hello, I am Alice",
  "profile_picture": "https://example.com/alice.jpg"
}
```

Success response includes:
- `token`
- `user` object

### 2) Login
`POST /login`

Request body example:

```json
{
  "username": "alice",
  "password": "strongpass123"
}
```

Success response includes:
- `token`
- `user` object

### 3) Profile
`GET /profile` (authenticated)

Returns current authenticated user's profile.

`PUT /profile` or `PATCH /profile` (authenticated)

Update fields such as:
- `first_name`
- `last_name`
- `email`
- `bio`
- `profile_picture`

### 4) Create Post
`POST /api/posts/`

```json
{
  "title": "My first post",
  "content": "Hello social API"
}
```

### 5) List Posts (Paginated + Search)
`GET /api/posts/`

- Pagination: `?page=1`
- Search by title/content: `?search=hello`

Example:

`GET /api/posts/?search=first&page=1`

### 6) Create Comment
`POST /api/comments/`

```json
{
  "post": 1,
  "content": "Nice post!"
}
```

### 7) Update/Delete Ownership Rule
- Only the post author can update/delete that post.
- Only the comment author can update/delete that comment.

## Testing with Postman
1. Register a user using `POST /register`.
2. Copy the returned token.
3. Call `GET /profile` with header `Authorization: Token <token>`.
4. Test `POST /login` with existing credentials and verify token is returned.
5. Test `POST /api/posts/`, `GET /api/posts/?search=<term>`.
6. Test `POST /api/comments/` using a valid post id.
7. Confirm author-only permissions by trying to edit/delete another user's post/comment.

## Automated Testing Results
Executed:

```bash
python manage.py check
python manage.py test
```

Result:
- System check passed with no issues.
- 6 tests passed (authentication + posts/comments CRUD/permissions/pagination/search).

## Project Structure

```text
social/
  manage.py
  db.sqlite3
  README.md
  social_media_api/
    settings.py
    urls.py
    asgi.py
    wsgi.py
  accounts/
    admin.py
    apps.py
    models.py
    serializers.py
    views.py
    urls.py
    migrations/
      0001_initial.py
  posts/
    admin.py
    apps.py
    models.py
    serializers.py
    permissions.py
    views.py
    urls.py
    migrations/
      0001_initial.py
```
