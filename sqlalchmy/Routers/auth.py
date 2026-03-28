from fastapi import APIRouter, Depends, status, HTTPException
# Oauth2PasswordRequestForm is used for authentication using email and password 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import model, utils, oauth2

# Create router for authentication-related endpoints
router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)
"""
    LOGIN ENDPOINT

    WHAT:
    -----
    Authenticates a user using email (passed as username) and password.

    WHY:
    ----
    - We use OAuthPasswordRequestForm because FastAPI follows OAuth2 standards.
    - OAuth2 expects 'username' and 'password', not 'email'.
    - So we pass email inside 'username' field.

    HOW:
    ----
    1. Extract credentials from request form.
    2. Query database to find user with given email.
    3. Verify password using hashing.
    4. Generate JWT access token.
    5. Return token to client.
    """
@router.post('/login')
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):

    # STEP 1: Fetch user from DB using email
    # NOTE: OAuth form uses 'username', so we treat it as email
    user = db.query(model.User).filter(
        model.User.email == user_credentials.username
    ).first()

    # STEP 2: If user does not exist → raise error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # STEP 3: Verify password
    # WHY: We never store plain passwords → always hashed
    # utils.verify() compares plain password with hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # STEP 4: Create JWT token
    # WHY: Token is used for authentication in future requests
    # HOW: We pass user_id inside token payload
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    # STEP 5: Return token
    # 'bearer' means token will be used in Authorization header
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }