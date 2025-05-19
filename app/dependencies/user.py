from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.dependencies.get_db import connection
from app.utils.tokens import SECRET_KEY, ALGORITHM
from sqlalchemy.future import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: AsyncSession = Depends(connection)
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="User ID missing in token")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token decode failed: {str(e)}")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user