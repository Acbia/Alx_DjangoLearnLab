# Django Blog Authentication System

## Features
- User Registration with email
- Login and Logout
- Profile view and email update

## How to Test
1. Visit `/register` to create a new account.
2. After registration, you’ll be redirected to `/profile`.
3. Visit `/login` to log in.
4. Visit `/logout` to log out.
5. On `/profile`, update your email and submit.

## Security
- CSRF protection enabled on all forms.
- Passwords hashed using Django’s default system.
- Profile view restricted to authenticated users.