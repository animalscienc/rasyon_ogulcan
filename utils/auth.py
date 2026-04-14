# Authentication Utilities for Zootekni Pro
# Password hashing and user authentication

import hashlib
import secrets
from typing import Optional

# Simple salt for password hashing (in production, use proper salt per user)
DEFAULT_SALT = "zootekni_pro_salt_2024"


def hash_password(password: str, salt: str = DEFAULT_SALT) -> str:
    """
    Hash password using SHA-256 with salt.
    
    Args:
        password: Plain text password
        salt: Salt string
        
    Returns:
        Hashed password
    """
    combined = f"{salt}{password}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()


def verify_password(password: str, password_hash: str, salt: str = DEFAULT_SALT) -> bool:
    """
    Verify password against hash.
    
    Args:
        password: Plain text password to verify
        password_hash: Stored password hash
        salt: Salt used in hashing
        
    Returns:
        True if password matches
    """
    return hash_password(password, salt) == password_hash


def generate_token(length: int = 32) -> str:
    """Generate random token."""
    return secrets.token_urlsafe(length)


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty"
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    if not username.isalnum():
        return False, "Username must contain only letters and numbers"
    return True, None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"
    if len(password) < 4:
        return False, "Password must be at least 4 characters"
    return True, None
