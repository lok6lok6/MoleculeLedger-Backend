# app/models/user_models.py

from pydantic import BaseModel, Field
from typing import Optional

# Purpose: Defines the data structure for a new user registration request.
# Architectural Role: Used by the FastAPI authentication routes (e.g., auth_routes.py)
# to validate the incoming JSON payload when a user attempts to register.
# Best Practice: Passwords should always be handled securely (hashed on the backend),
# and Pydantic helps ensure they're present during input.
class UserCreate(BaseModel):
    email: str = Field(..., example="scientist@example.com")
    password: str = Field(..., example="SecurePassword123")

# Purpose: Defines the data structure for a user login request.
# Architectural Role: Similar to UserCreate, used by auth_routes.py for login validation.
class UserLogin(BaseModel):
    email: str = Field(..., example="scientist@example.com")
    password: str = Field(..., example="SecurePassword123")

# Purpose: Defines the structure of the JWT token response sent back to the client
# after successful login or registration.
# Architectural Role: This model dictates how the AuthService returns authentication
# tokens to the frontend.
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" # Default to "bearer" as is common with JWTs

# Purpose: Defines a simplified representation of a user for API responses,
# omitting sensitive information like the password hash.
# Architectural Role: Used when the backend needs to return user details (e.g.,
# after registration or for a user profile endpoint). Prevents exposing sensitive data.
class UserResponse(BaseModel):
    id: int
    email: str

    # Pydantic's 'from_attributes' mode (formerly 'orm_mode') allows Pydantic models
    # to read data directly from ORM models (like SQLAlchemy models, which we'll use later).
    # This makes it easy to convert database objects into API-friendly formats.
    class Config:
        from_attributes = True # Equivalent to orm_mode = True in older Pydantic