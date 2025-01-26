import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Header
from typing import Optional
from models.person import Person

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

class AuthService:
    def generate_user_token(self, person: Person) -> str:
        payload = {"name": person.name}
        expire = datetime.now(timezone.utc) + timedelta(days=1) 
        payload["exp"] = expire.timestamp()
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    async def authenticate(authorization: Optional[str] = Header(None)) -> bool:
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        try:
            token = authorization.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, IndexError):
            raise HTTPException(status_code=401, detail="Invalid or expired token")