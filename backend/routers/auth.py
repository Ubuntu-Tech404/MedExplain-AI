from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, Dict
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# In production, use environment variables
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Demo users (in production, use database)
DEMO_USERS = {
    "demo@mediclinic.com": {
        "id": "demo-patient-001",
        "email": "demo@mediclinic.com",
        "name": "Demo Patient",
        "password": "demo123",  # In production, use hashed passwords
        "role": "patient",
        "created_at": "2024-01-01T00:00:00"
    },
    "doctor@mediclinic.com": {
        "id": "demo-doctor-001",
        "email": "doctor@mediclinic.com",
        "name": "Dr. Smith",
        "password": "doctor123",
        "role": "doctor",
        "specialty": "Endocrinology",
        "created_at": "2024-01-01T00:00:00"
    }
}

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(authorization: str = Header(None)):
    """Verify JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/login")
async def login(email: str, password: str):
    """User login"""
    try:
        # Check demo users
        user = DEMO_USERS.get(email)
        
        if not user or user["password"] != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"], "role": user["role"], "user_id": user["id"]},
            expires_delta=access_token_expires
        )
        
        # Remove password from response
        user_response = user.copy()
        user_response.pop("password", None)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user_response
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register(
    email: str,
    password: str,
    name: str,
    role: str = "patient",
    specialty: Optional[str] = None
):
    """User registration (demo only)"""
    try:
        # Check if user already exists
        if email in DEMO_USERS:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user (in demo only)
        new_user = {
            "id": f"user-{datetime.now().timestamp()}",
            "email": email,
            "name": name,
            "password": password,  # In production, hash this
            "role": role,
            "created_at": datetime.now().isoformat()
        }
        
        if role == "doctor" and specialty:
            new_user["specialty"] = specialty
        
        # In production, save to database
        # For demo, just add to DEMO_USERS
        DEMO_USERS[email] = new_user
        
        # Create token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_user["email"], "role": new_user["role"], "user_id": new_user["id"]},
            expires_delta=access_token_expires
        )
        
        # Remove password from response
        user_response = new_user.copy()
        user_response.pop("password", None)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user_response
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_current_user(payload: Dict = Depends(verify_token)):
    """Get current user information"""
    try:
        email = payload.get("sub")
        user = DEMO_USERS.get(email)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Remove password from response
        user_response = user.copy()
        user_response.pop("password", None)
        
        return {"user": user_response}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout")
async def logout():
    """User logout (client-side token invalidation)"""
    return {"message": "Successfully logged out"}

@router.get("/roles")
async def get_roles():
    """Get available user roles"""
    return {
        "roles": [
            {"id": "patient", "name": "Patient", "description": "Medical patient"},
            {"id": "doctor", "name": "Doctor", "description": "Healthcare provider"},
            {"id": "nurse", "name": "Nurse", "description": "Nursing staff"},
            {"id": "admin", "name": "Administrator", "description": "System administrator"}
        ]
    }

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token (simplified for demo)"""
    # In production, implement proper refresh token logic
    try:
        # Verify refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if not email or email not in DEMO_USERS:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        user = DEMO_USERS[email]
        
        # Create new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": user["email"], "role": user["role"], "user_id": user["id"]},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))