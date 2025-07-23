# app/services/auth_service.py

from datetime import timedelta
from typing import Optional

# Import the Pydantic models we defined for users and tokens.
from app.models.user_models import UserCreate, UserLogin, UserResponse, Token

# Import our security utilities for password hashing and JWT handling.
from app.core.security import verify_password, get_password_hash, create_access_token

# (Temporary) Placeholder for database operations.
# In a real application, this would interact with crud.py to save/retrieve users.
# Using a dictionary to simulate a database for now,
# to focus on the authentication logic flow.
# Best Practice: This 'fake_users_db' should be replaced by actual database integration.
fake_users_db = {} # type: dict[str, dict] # Maps email to user data (id, email, hashed_password)
user_id_counter = 1

class AuthService:
    """
    AuthService handles the core business logic for user registration and login.
    It orchestrates the use of Pydantic models for data validation,
    security utilities for password hashing and JWT creation, and
    (eventually) database operations.
    """

    async def register_user(self, user_create: UserCreate) -> Optional[UserResponse]:
        """
        Registers a new user.
        Hashes the password and (temporarily) stores the user.
        """
        # Best Practice: Check if user already exists before registering.
        if user_create.email in fake_users_db:
            # In a real app, you'd raise an HTTPException here.
            return None # Indicates user already exists or registration failed

        # Hash the plain-text password using our security utility.
        hashed_password = get_password_hash(user_create.password)

        global user_id_counter # Access the global counter
        new_user = {
            "id": user_id_counter,
            "email": user_create.email,
            "hashed_password": hashed_password
        }
        fake_users_db[user_create.email] = new_user
        user_id_counter += 1

        # Return a UserResponse model, which does NOT include the hashed password.
        return UserResponse(id=new_user["id"], email=new_user["email"])

    async def authenticate_user(self, user_login: UserLogin) -> Optional[UserResponse]:
        """
        Authenticates a user based on email and password.
        """
        user_data = fake_users_db.get(user_login.email)
        if not user_data:
            return None # User not found

        # Verify the provided password against the stored hash.
        if not verify_password(user_login.password, user_data["hashed_password"]):
            return None # Incorrect password

        return UserResponse(id=user_data["id"], email=user_data["email"])

    async def create_user_access_token(self, user_email: str) -> Token:
        """
        Creates a JWT access token for an authenticated user.
        """
        # Define token expiration. This can be configured in app/core/security.py
        # or passed in. We'll use the default from security.py for now.
        # Best Practice: Short-lived access tokens require refresh tokens (future scope).
        token_expires = timedelta(minutes=30) # Example duration

        # Create the data payload for the JWT. 'sub' (subject) is a standard JWT claim.
        token_data = {"sub": user_email}

        # Use our security utility to create the JWT.
        access_token = create_access_token(
            data=token_data, expires_delta=token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

# Instantiate the service. This can be done directly or via FastAPI's dependency injection later.
auth_service = AuthService()