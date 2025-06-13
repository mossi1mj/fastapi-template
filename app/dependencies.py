from fastapi import Header, HTTPException, Depends
from typing import Optional
import logging
import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

logger = logging.getLogger(__name__)
service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

if not service_account_path:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_PATH not set in environment.")

def initialize_firebase():
    if not firebase_admin._apps:
        logger.info("Initializing Firebase Admin SDK")
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized successfully")
    else:
        logger.info("Firebase already initialized")

def verify_firebase_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Verifies Firebase JWT token sent via Authorization header.

    The frontend must send:
    Authorization: Bearer <id_token>
    """
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Authorization header missing or malformed")
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header.")

    id_token = authorization.split(" ")[1]
    logger.info("Verifying Firebase token")

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        logger.info(f"Firebase token verified for UID: {uid}")
        return uid
    except Exception as e:
        logger.warning(f"JWT validation failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid Firebase token.")