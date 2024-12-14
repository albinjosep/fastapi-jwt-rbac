from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Any, Dict
from fastapi import HTTPException

# Secret key to encode and decode JWT tokens
SECRET_KEY = "R0pdMSU6-8NXwmraRGUNyAmt2UJDrYTEJV80g2pgjqQ"  # Should be in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

def create_access_token(data: Dict[str, Any], expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token has expired or is invalid.")
