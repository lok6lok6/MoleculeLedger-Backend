# app/api/v1/auth_routes.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user_models import UserCreate, UserLogin, Token, UserResponse # Import our Pydantic models
from app.services.auth_service import auth_service # Import our AuthService instance

# Purpose: APIRouter allows us to organize API endpoints into modular components.
# Architectural Role: This router will be 'included' in our main FastAPI app (main.py)
# allowing us to separate concerns and scale our API.
router = APIRouter(
    prefix="/auth", # All routes in this router will start with /auth
    tags=["Authentication"] # Used for OpenAPI documentation (Swagger UI)
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate):
    """
    Register a new user account.
    Best Practice: Return UserResponse which does not include the password hash.
    """
    # Architectural Role: Delegates the business logic to the auth_service.
    new_user = await auth_service.register_user(user_create)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # 409 Conflict if user already exists
            detail="Email already registered"
        )
    return new_user

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    """
    Authenticate a user and return an access token.
    Best Practice: JWTs are stateless and are the standard for API authentication.
    """
    # Architectural Role: Delegates authentication logic to the auth_service.
    user = await auth_service.authenticate_user(user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, # 401 Unauthorized for invalid credentials
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Architectural Role: Uses auth_service to create the JWT.
    token = await auth_service.create_user_access_token(user_email=user.email)
    return token