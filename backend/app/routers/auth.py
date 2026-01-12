from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, AuthResponse, UserResponse, Token
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user account."""
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return tokens."""
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    
    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Get new access token using refresh token."""
    payload = decode_token(refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return UserResponse.model_validate(current_user)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout current user (client should discard tokens)."""
    return {"message": "Successfully logged out"}
