Django Built-in Authentication
This project demonstrates how to implement Django's built-in authentication system, including user registration, login, logout, and password management.

Features
User Registration

Login & Logout

Password Reset via Email

Password Change

Access Control (Login Required)

Prerequisites
Python 3.8+

Django 4.x+

SQLite (default) or any Django-supported database

Setup Instructions
1. Clone the Repository
by using:
git clone https://github.com/yourusername/django-auth-example.git

cd django-auth-example
3. Create a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
4. Install Dependencies
bash
Copy code
pip install -r requirements.txt
5. Apply Migrations
bash
Copy code
python manage.py migrate
6. Create a Superuser (Optional)
bash
Copy code
python manage.py createsuperuser
7. Run the Server
bash
Copy code
python manage.py runserver
URL Routes
Path	View	Description
/accounts/login/	LoginView	User login
/accounts/logout/	LogoutView	User logout
/accounts/password_change/	PasswordChangeView	Change password
/accounts/password_reset/	PasswordResetView	Reset password
/register/	Custom View	User registration (manual)
