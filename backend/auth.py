from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError

from config import settings
from utils.security import SecurityUtils

security = HTTPBearer()

class AuthService:
    """Authentication service"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=30)  # Refresh tokens last 30 days
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify token and return payload"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except InvalidTokenError:
            return None
    
    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Get current user from token"""
        token = credentials.credentials
        payload = AuthService.verify_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    
    @staticmethod
    def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
        """Get current active user"""
        # Check if user is active (you can add more checks here)
        if current_user.get("disabled", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user
    
    @staticmethod
    def get_current_user_if_exists(credentials: Optional[HTTPAuthorizationCredentials] = None) -> Optional[Dict[str, Any]]:
        """Get current user if token exists, otherwise return None"""
        if credentials:
            return AuthService.get_current_user(credentials)
        return None
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[str]:
        """Refresh access token using refresh token"""
        payload = AuthService.verify_token(refresh_token)
        
        if payload is None or payload.get("type") != "refresh":
            return None
        
        # Create new access token with same data (excluding token-specific fields)
        user_data = {k: v for k, v in payload.items() if k not in ["exp", "iat", "type"]}
        new_access_token = AuthService.create_access_token(user_data)
        
        return new_access_token
    
    @staticmethod
    def hash_password(password: str) -> tuple:
        """Hash password"""
        return SecurityUtils.hash_password(password)
    
    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """Verify password"""
        return SecurityUtils.verify_password(password, hashed_password, salt)

# Demo user database (in production, use real database)
DEMO_USERS = {
    "demo@mediclinic.com": {
        "id": "demo-patient-001",
        "email": "demo@mediclinic.com",
        "name": "Demo Patient",
        "password_hash": "hashed_password_here",
        "password_salt": "salt_here",
        "role": "patient",
        "disabled": False,
        "created_at": "2024-01-01T00:00:00"
    },
    "doctor@mediclinic.com": {
        "id": "demo-doctor-001",
        "email": "doctor@mediclinic.com",
        "name": "Dr. Smith",
        "password_hash": "hashed_password_here",
        "password_salt": "salt_here",
        "role": "doctor",
        "specialty": "Endocrinology",
        "disabled": False,
        "created_at": "2024-01-01T00:00:00"
    },
    "admin@mediclinic.com": {
        "id": "demo-admin-001",
        "email": "admin@mediclinic.com",
        "name": "Admin User",
        "password_hash": "hashed_password_here",
        "password_salt": "salt_here",
        "role": "admin",
        "disabled": False,
        "created_at": "2024-01-01T00:00:00"
    }
}

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email (demo version)"""
    return DEMO_USERS.get(email)

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user (demo version)"""
    user = get_user_by_email(email)
    if not user:
        return None
    
    # In production, verify password hash
    # For demo, use simple password check
    if password == "demo123" and email == "demo@mediclinic.com":
        return user
    elif password == "doctor123" and email == "doctor@mediclinic.com":
        return user
    elif password == "admin123" and email == "admin@mediclinic.com":
        return user
    
    return None