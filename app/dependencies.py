from fastapi import Header, HTTPException, Depends
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def get_current_user_uid(x_user_uid: Optional[str] = Header(None)) -> str:
    """
    Dependency that extracts the Firebase UID from the 'X-User-Uid' header.

    Frontend must send the UID in this custom header:
        X-User-Uid: firebase_uid_here
    """
    if not x_user_uid:
        logger.warning("Missing X-User-Uid header in request.")
        raise HTTPException(status_code=401, detail="Missing user UID.")
    return x_user_uid
