

# LibraryProject 📚

This is a simple Django project I’m building to learn how Django works. It’s part of my ALX Django learning journey and will eventually become a basic library management system. Right now, it just sets up the Django project and runs the server.

---

## 🚀 Getting Started

### ✅ Requirements:

* Python 3.8+
* pip (comes with Python)
* Git
* Code editor (like VS Code)

---

### 🔧 Setup Instructions:

1. **Install Django**

   ```
   pip install django
   ```

2. **Start Project**

   ```
   django-admin startproject LibraryProject
   ```

3. **(Optional) Set up a virtual environment**

   ```
   python -m venv env
   # Activate:
   # Windows: env\Scripts\activate
   # Mac/Linux: source env/bin/activate
   ```

4. **Run the server**

   ```
   cd LibraryProject
   python manage.py runserver
   ```

5. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000)
   You should see the default Django welcome page!

---

## 📁 Project Files

* `manage.py` – controls your project
* `settings.py` – main config
* `urls.py` – handles routing
* `asgi.py / wsgi.py` – server stuff

---

## ⏭️ What’s Next?

* Create apps using:

  ```
  python manage.py startapp bookshelf
  ```
* Add models, views, and URLs
* Learn more from the [Django docs](https://docs.djangoproject.com/en/stable/)

---

## 🤝 Contributing

This is part of my repo: [Alx\_DjangoLearnLab](https://github.com/RedietSeleshiTsega/Alx_DjangoLearnLab)
Feel free to fork it and try things out!


# Permissions and Groups Setup

## Groups Configuration
- **Editors**: Assigned `can_create` and `can_edit` permissions for the Book model.
- **Viewers**: Assigned `can_view` permission for the Book model.
- **Admins**: Assigned all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`).

## Setup Instructions
1. Create groups via Django Admin (`/admin/auth/group/`).
2. Assign permissions to groups (e.g., `bookshelf.can_view`, `bookshelf.can_create`).
3. Assign users to groups via Django Admin.
4. Test permissions by logging in as different users and attempting to access views.

## Testing
- Create test users and assign them to different groups (e.g., Viewer, Editor).
- Verify that users can only perform actions allowed by their group permissions.
