import hashlib
import secrets
import string
from typing import Optional, Tuple, List
import jwt
from datetime import datetime, timedelta
import os
import re

from config import settings

class SecurityUtils:
    """Security utility functions"""
    
    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        salted_password = salt + password
        hashed = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashed, salt
    
    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against hash and salt"""
        salted_password = salt + password
        test_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        return test_hash == hashed_password
    
    @staticmethod
    def generate_api_key(length: int = 32) -> str:
        """Generate random API key"""
        alphabet = string.ascii_letters + string.digits + "-_"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_secure_token(length: int = 64) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def sanitize_input(text: str, allowed_tags: Optional[List[str]] = None) -> str:
        """Sanitize user input to prevent XSS attacks"""
        if not text:
            return text
        
        # Basic XSS prevention
        replacements = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;',
            '\\': '&#x5C;',
            '`': '&#x60;',
            '(': '&#40;',
            ')': '&#41;',
            '&': '&amp;'
        }
        
        # Allow certain HTML tags if specified
        if allowed_tags:
            # This is a simplified version - use a proper HTML sanitizer in production
            sanitized = text
            for tag in allowed_tags:
                pattern = f'<{tag}[^>]*>|</{tag}>'
                sanitized = re.sub(pattern, '', sanitized)
            
            # Apply basic replacements to remaining text
            for old, new in replacements.items():
                sanitized = sanitized.replace(old, new)
            
            return sanitized
        
        # Apply all replacements
        sanitized = text
        for old, new in replacements.items():
            sanitized = sanitized.replace(old, new)
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_strong_password(password: str) -> Tuple[bool, List[str]]:
        """Check if password meets security requirements"""
        errors = []
        
        # Length check
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        # Uppercase check
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        # Lowercase check
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        # Digit check
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        # Special character check
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        if not any(c in special_chars for c in password):
            errors.append(f"Password must contain at least one special character ({special_chars})")
        
        # Common password check (simplified)
        common_passwords = {'password', '123456', 'qwerty', 'letmein', 'welcome'}
        if password.lower() in common_passwords:
            errors.append("Password is too common")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def generate_jwt_token(payload: dict, expires_minutes: int = None) -> str:
        """Generate JWT token"""
        if expires_minutes is None:
            expires_minutes = settings.access_token_expire_minutes
        
        payload_copy = payload.copy()
        payload_copy["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
        payload_copy["iat"] = datetime.utcnow()
        
        return jwt.encode(payload_copy, settings.secret_key, algorithm=settings.algorithm)
    
    @staticmethod
    def verify_jwt_token(token: str) -> Optional[dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def generate_password_reset_token(email: str) -> str:
        """Generate password reset token"""
        payload = {
            "email": email,
            "type": "password_reset",
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return SecurityUtils.generate_jwt_token(payload)
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[str]:
        """Verify password reset token and return email"""
        payload = SecurityUtils.verify_jwt_token(token)
        if payload and payload.get("type") == "password_reset":
            return payload.get("email")
        return None
    
    @staticmethod
    def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
        """Mask sensitive data (e.g., credit cards, SSN)"""
        if len(data) <= visible_chars * 2:
            return '*' * len(data)
        
        first_part = data[:visible_chars]
        last_part = data[-visible_chars:] if visible_chars > 0 else ''
        masked_middle = '*' * (len(data) - visible_chars * 2)
        
        return f"{first_part}{masked_middle}{last_part}"
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Validate phone number format"""
        # Simple validation - adjust based on requirements
        pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$'
        return bool(re.match(pattern, phone))