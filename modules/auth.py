# modules/auth.py
import streamlit as st
import hashlib
import re
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Set up the SQLite database connection
engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a User model for our database
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # In production, use a robust password hashing method.
    role = Column(String, default="user")  # Role can be used for authorization (e.g., admin, user)

def init_db():
    """
    Initialize the database and create tables if they do not exist.
    """
    Base.metadata.create_all(bind=engine)

def hash_password(password):
    """
    Hash the provided password using SHA256.
    (Note: For production use, consider more secure hashing algorithms like bcrypt.)
    """
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role="user"):
    """
    Register a new user. Returns a tuple: (success, message).
    """
    db = SessionLocal()
    # Check if the username already exists.
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        db.close()
        return False, "Username already exists."
    # Create a new user with the hashed password.
    new_user = User(username=username, password=hash_password(password), role=role)
    db.add(new_user)
    db.commit()
    db.close()
    return True, "User registered successfully."

def authenticate_user(username, password):
    """
    Authenticate a user against the database.
    Returns a tuple: (True/False, role or None).
    """
    db = SessionLocal()
    user = db.query(User).filter(
        User.username == username,
        User.password == hash_password(password)
    ).first()
    db.close()
    if user:
        return True, user.role
    return False, None

# ---------------------- Validation Functions ---------------------- #

def validate_username(username):
    """
    Validates the username.
    - Must not be empty.
    - Must be at least 3 characters long.
    - Can only contain letters, numbers, and underscores.
    """
    if not username or username.strip() == "":
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not re.match("^[A-Za-z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""

def validate_password(password):
    """
    Validates the password.
    - Must not be empty.
    - Must be at least 8 characters long.
    - Must contain at least one uppercase letter, one lowercase letter, and one number.
    """
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    return True, ""

# ---------------------- Login / Registration UI ---------------------- #

def login():
    """
    Display the login (and registration) form and handle user authentication.
    """
    st.title("User Login / Registration")
    st.write("Please log in or register to access the Refugee Campaign AI Platform.")

    # Input fields for username and password.
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Buttons for login and registration actions.
    login_button = st.button("Login")
    register_button = st.button("Register")

    # Process the login button click.
    if login_button:
        if not username:
            st.error("Please enter your username.")
        elif not password:
            st.error("Please enter your password.")
        else:
            success, role = authenticate_user(username, password)
            if success:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role
                st.success(f"Logged in as {username} ({role})")
            else:
                st.error("Invalid credentials. Please try again.")

    # Process the registration button click.
    if register_button:
        # Validate username and password before registration.
        valid_username, username_error = validate_username(username)
        valid_password, password_error = validate_password(password)
        
        if not valid_username:
            st.error(username_error)
        elif not valid_password:
            st.error(password_error)
        else:
            success, msg = register_user(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)
