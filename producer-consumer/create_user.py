from airflow import models
from airflow.secrets import fernet
from airflow.utils import timezone

username = input("Enter the username: ")
password_str = input("Enter the password: ")
email = input("Enter the email address: ")

fernet_key = fernet.generate_key()
fernet_instance = fernet.Fernet(fernet_key)

user = models.User(
    username=username,
    email=email,
    is_superuser=True,
    is_active=True,
    # Encrypt and hash the user's password using a secure encryption algorithm
    password=fernet_instance.encrypt(password_str.encode()).decode(),
    # Set the user's created_at and updated_at fields to the current timestamp
    # to avoid "null" value errors
    created_at=timezone.utcnow(),
    updated_at=timezone.utcnow(),
)

session = models.Session()
session.add(user)
session.commit()
session.close()

print("User created.")
