from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# Example users database
users_db = {
    "admin": {"username": "admin", "password": "password", "role": "Admin"},
    "alice": {"username": "alice", "password": "researcherpass", "role": "Researcher"},
    "bob": {"username": "bob", "password": "viewerpass", "role": "Viewer"},
}

roles_hierarchy = {"Admin": 3, "Researcher": 2, "Viewer": 1}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    user = users_db.get(username)
    if user and user["password"] == password:
        return user
    return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        role: str = payload.get("role")
        if role is None:
            raise credentials_exception
        user = users_db.get(username)
        if user is None or user["role"] != role:
            raise credentials_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception

def require_role(required_role: str):
    def role_checker(user: Dict = Depends(get_current_user)):
        user_role = user["role"]
        if roles_hierarchy[user_role] < roles_hierarchy[required_role]:
            raise HTTPException(status_code=403, detail=f"Requires {required_role} role")
        return user
    return role_checker

# FastAPI login endpoint example
from fastapi import APIRouter
router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"} 