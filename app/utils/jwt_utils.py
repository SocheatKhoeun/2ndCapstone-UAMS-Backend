import time
from typing import Optional, Tuple

import jwt
from fastapi import HTTPException


def create_access_token(data: dict, secret: str, jwt_ttl: int, token_type: str = "access") -> Tuple[str, int]:
    """Create a JWT and include a token_type claim (access|refresh).

    Returns (token, expires_unix).
    """
    to_encode = data.copy()
    expire = int(time.time()) + int(jwt_ttl)
    # include expiry and explicit token type
    to_encode.update({"exp": expire, "token_type": token_type})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")
    return encoded_jwt, expire


def decode_access_token(token: str, secret: str):
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"]) if token else None
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
