# app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Union, Any

# passlib is used for password hashing, and bcrypt is the specific algorithm.
# It's a best practice to never store plain text passwords.
from passlib.context import CryptContext

# python-jose is used for handling JSON Web Tokens (JWTs).
# JWTs are used for stateless authentication.
from jose import jwt, JWTError

# We need access to environment variables for our JWT secret key.
import os
from dotenv import load_dotenv

# Load environment variables (ensure this is done once at app startup in main.py,
# but good to have here for script testing or if this module is run independently)
load_dotenv()

# ---- Configuration ---
# Best Practice: JWT_SECRET_KEY should be a strong, randomly generated string
# and kept absolutely secret, loaded from environment variables.
# Algorithms: HS256 is a common symmetric algorithm for JWTs.
# ACCESS_TOKEN_EXPIRE_MINUTES: Defines how long the access token is valid.
# Shorter lifespans enhance security by reducing the window for token misuse.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not found in .env file. Please generate one.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # For example, 30 minutes until token expires.

# Password hashing context. Schemes define the hashing algorithm to use.
# Best Practice: bcrypt is computationally intensive, making brute-force attacks harder.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Hashing Functions ---
# Purpose: Provides a secure way to hash and verify passwords.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain-text password matches a hashed password.
    """
    # Best Practice: The verify() method handles the salt generation and hashing internally.
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password.
    """
    # Best Practice: The hash() method generates a new hash each time,
    # including a random salt, which prevents rainbow table attacks.
    return pwd_context.hash(password)

# --- JWT Token Functions ---
# Purpose: Creates and handles the lifecycle of JWTs.
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Creates a JWT access token.
    data: Payload to be encoded into the token (e.g., user ID).
    expires_delta: Optional timedelta for custom expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # jwt.encode: Takes the payload, secret key, and algorithm to create the token.
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# No specific decode_access_token function here yet, as FastAPI's dependency
# injection will handle token validation using OAuth2PasswordBearer, which
# internally leverages jose.jwt.decode. Will implement that in dependencies.py.