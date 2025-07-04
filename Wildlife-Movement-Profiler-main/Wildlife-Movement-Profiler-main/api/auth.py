# Authentication utilities for FastAPI API
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
SECRET_KEY = "secret"
ALGORITHM = "HS256"

# Helper to create JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dummy user authentication for demonstration
def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user (dummy logic for demo)."""
    if username == "admin" and password == "password":
        return {"username": username}
    return None

# Dependency to get current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """Decode JWT token and return user info."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"username": username}
    except JWTError:
        raise credentials_exception

# Role-based access control (not used in demo, but provided for extension)
def require_role(required_role: str):
    """Dependency to require a specific user role (for future use)."""
    def role_checker(user: Dict = Depends(get_current_user)):
        # Dummy: all users are 'admin' in this demo
        if required_role != "admin":
            raise HTTPException(status_code=403, detail=f"Requires {required_role} role")
        return user
    return role_checker

# Login endpoint (for demonstration)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token (for demonstration)."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"} 