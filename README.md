# Social Media API

This is a Django + Django REST Framework social media API with custom user authentication, posts, comments, likes, follows, and notifications.

## Tech Stack
- Python 3
- Django
- Django REST Framework
- DRF Token Authentication
- SQLite (default)

## Implemented Features
- Custom user model (`accounts.User`) with:
  - `bio`
  - `profile_picture`
  - follower/following relation
- Authentication endpoints:
  - `POST /register`
  - `POST /login`
  - `GET /profile`
  - `PUT/PATCH /profile`
- Follow system:
  - `POST /users/<user_id>/follow/`
  - `POST /users/<user_id>/unfollow/`
- Posts and comments:
  - `GET/POST /api/posts/`
  - `GET/PUT/PATCH/DELETE /api/posts/<id>/`
  - `GET/POST /api/comments/`
  - `GET/PUT/PATCH/DELETE /api/comments/<id>/`
- Like system:
  - `POST /api/posts/<id>/like/`
  - `POST /api/posts/<id>/unlike/`
  - Duplicate likes are prevented by DB constraint and view logic.
- Notification system:
  - Notifications are created for:
    - new followers
    - likes on your posts
    - comments on your posts
  - `GET /notifications/` (unread first)
  - `GET /notifications/?unread=true` (only unread)
  - `POST /notifications/<id>/read/`

## Setup
1. Install dependencies:

```bash
pip install django djangorestframework
```

2. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Run the server:

```bash
python manage.py runserver
```

## Authentication
Use token authentication for protected endpoints:

```http
Authorization: Token <your_token>
```

## API Examples

### Like a post
`POST /api/posts/1/like/`

Response:

```json
{
  "detail": "Post liked."
}
```

### Unlike a post
`POST /api/posts/1/unlike/`

Response:

```json
{
  "detail": "Post unliked."
}
```

### Follow a user
`POST /users/2/follow/`

Response:

```json
{
  "detail": "Now following this user."
}
```

### Fetch notifications
`GET /notifications/`

Response item shape:

```json
{
  "id": 1,
  "actor": 2,
  "actor_username": "alice",
  "verb": "liked your post",
  "target_type": "post",
  "target_id": 7,
  "target_repr": "My Post by bob",
  "is_read": false,
  "timestamp": "2026-02-21T10:00:00Z"
}
```

## Testing
Automated tests cover:
- authentication flow
- post/comment CRUD permissions
- like/unlike flow
- notification generation for follow/like/comment
- notification listing and mark-as-read behavior

Run:

```bash
python manage.py test
```

## Project Structure

```text
social_media_api/
  manage.py
  db.sqlite3
  README.md
  social_media_api/
    settings.py
    urls.py
    asgi.py
    wsgi.py
  accounts/
  posts/
  notifications/
```
