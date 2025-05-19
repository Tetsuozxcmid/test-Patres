from jose import jwt
from datetime import datetime,timedelta,timezone
from core.config import get_auth_data
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def create_access_token(data: dict) ->str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp" : expire })
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode,auth_data['secret_key'],algorithm=auth_data['algorithm'])
    return encode_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),security: HTTPAuthorizationCredentials = Depends(security) ): 
    pass

