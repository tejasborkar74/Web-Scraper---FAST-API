import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Header
from typing import Optional
from models.person import Person
from config.config_loader import load_config

config = load_config()

class AuthService:
    def generate_user_token(self, person: Person) -> str:
        payload = {"name": person.name}
        expire = datetime.now(timezone.utc) + timedelta(days=1) 
        payload["exp"] = expire.timestamp()
        token = jwt.encode(payload, config["JWT_SECRET_KEY"], algorithm=config["JWT_ALGORITHM"])
        return token

    @staticmethod
    async def authenticate(authorization: Optional[str] = Header(None)) -> bool:
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        try:
            token = authorization.split(" ")[1]
            jwt.decode(token, config["JWT_SECRET_KEY"], algorithms=[config["JWT_ALGORITHM"]])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, IndexError):
            raise HTTPException(status_code=401, detail="Invalid or expired token")