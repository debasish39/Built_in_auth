from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom manager to handle user creation (for custom user model)
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # Check if email is provided
        if not email:
            raise ValueError("User must have a valid email address...")

        # Normalize email (e.g., lowercase domain part)
        user = self.model(email=self.normalize_email(email))

        # Set the hashed password
        user.set_password(password)

        # Save user to the database
        user.save(using=self._db)
        return user  

    def create_superuser(self, email, password=None, **extra_fields):
        # Set default fields required for superuser
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_superuser', True)      

        # Make sure is_staff is True
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        # Create user with email and password
        user = self.create_user(email, password)

        # Set superuser privileges manually
        user.is_staff = True
        user.is_superuser = True
        user.is_customer = True
        user.is_seller = True

        # Save changes
        user.save(using=self._db)
        return user


# Custom user model using AbstractUser (inherits username logic but you can override it)
class User(AbstractUser):
    # Use email as the primary field for login instead of username
    email = models.EmailField(max_length=255, unique=True)
    username = None  # <-- Add this line to remove the username field
    # Custom fields
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # Permission flags
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Custom role flags
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=True)

    # Auto-managed timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tell Django to use email as the unique identifier for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'city']
    # Connect to the custom manager
    objects = UserManager()

    # String representation of the user object
    def __str__(self):
        return self.email
