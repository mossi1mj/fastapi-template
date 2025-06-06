"""
Utility functions for authentication, including password hashing and verification.

These should be used in your user services when creating or verifying users.
"""

import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Hashes a plain password using bcrypt.
    
    Replace plain passwords with the hashed version before storing in DB.
    """
    salt = bcrypt.gensalt()  # Generates a random salt
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Store as string in DB

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the plain password matches the hashed version.
    
    Use this during login or authentication.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
