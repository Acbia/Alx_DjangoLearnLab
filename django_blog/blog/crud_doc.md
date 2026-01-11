# Blog Post Management Features

## Features
- Create, Read, Update, Delete posts
- Only authenticated users can create posts
- Only post authors can edit or delete their posts

## URLs
- `/` → List all posts
- `/posts/new/` → Create post
- `/posts/<pk>/` → View post
- `/posts/<pk>/edit/` → Edit post
- `/posts/<pk>/delete/` → Delete post

## Permissions
- Login required for create/edit/delete
- Only authors can modify their own posts