from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
from starlette import status
from starlette.responses import Response

from src.app.core.exceptions.user_exception import UserAccountError
from src.app.utils.schemas.user_schemas import UserSchema


def get_current_user(
        res: Response,
        credential: HTTPAuthorizationCredentials = Depends(
            HTTPBearer(auto_error=False)
        ),
) -> UserSchema:
    '''
    Get the current user based on the provided HTTP Authorization credentials.

Args:
    res (Response): The response object to set headers if needed.
    credential (HTTPAuthorizationCredentials): The HTTP Authorization credentials obtained from the request.

Returns:
    UserSchema: A UserSchema object containing the decoded user information.

Raises:
    HTTPException: If the credentials are missing.
    UserAccountError: If there are token verification errors such as RevokedIdTokenError, UserDisabledError, InvalidIdTokenError, or any other unexpected exceptions.
'''
    if credential is None:
        raise UserAccountError(
            message="Invalid token, please login again",
            error_code="REVOKED_TOKEN"
        )
    try:
        decoded_token = auth.verify_id_token(credential.credentials)
    except auth.RevokedIdTokenError:
        raise UserAccountError(
            message="Invalid token, please login again",
            error_code="REVOKED_TOKEN"
        )
    except auth.UserDisabledError:
        raise UserAccountError(
            message="Your account has been disabled, please contact support",
            error_code="USER_ACCOUNT_DISABLE"
        )
    except auth.InvalidIdTokenError:
        raise UserAccountError(
            message="Invalid token, please login again",
            error_code="INVALID_TOKEN"
        )
    except Exception as err:
        raise UserAccountError(
            message="Invalid token, please login again",
            error_code="INVALID_TOKEN"
        )
    res.headers["WWW-Authenticate"] = 'Bearer realm="auth_required"'
    return UserSchema(**decoded_token)
