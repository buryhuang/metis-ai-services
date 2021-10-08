"""Decorators that decode and verify authorization tokens."""
import jwt
from functools import wraps
from datetime import datetime, timezone, timedelta
from flask import request
from flask import current_app

from metis_ai_services.utils.result import Result
from metis_ai_services.api.exceptions import ApiUnauthorized, ApiForbidden
from metis_ai_services.utils.dynamodb_util import check_token

# from metis_ai_services.models.user import User


def encode_access_token(public_id):
    now = datetime.now(timezone.utc)
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expire = now + timedelta(hours=token_age_h, minutes=token_age_m)
    if current_app.config["TESTING"]:
        expire = now + timedelta(seconds=5)
    payload = dict(exp=expire, iat=now, sub=public_id)
    key = current_app.config.get("SECRET_KEY")
    return jwt.encode(payload, key, algorithm="HS256").encode("UTF-8")


def token_required(f):
    """Execute function if request contains valid access token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token(admin_only=False)
        for name, val in token_payload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    """Execute function if request contains valid access token AND user is admin."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token()
        if not token_payload["admin"]:
            raise ApiForbidden()
        for name, val in token_payload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated


def _check_access_token(admin_only=False):
    token = request.headers.get("Authorization")
    if not token:
        raise ApiUnauthorized(description="Unauthorized", admin_only=admin_only)
    result = decode_access_token(token)
    if result.failure:
        raise ApiUnauthorized(
            description=result.error,
            admin_only=admin_only,
            error="invalid_token",
            error_description=result.error,
        )
    return result.value


def decode_access_token(access_token):
    if isinstance(access_token, bytes):
        access_token = access_token.decode("ascii")
    if access_token.startswith("Bearer "):
        split = access_token.split("Bearer")
        access_token = split[1].strip()
    try:
        key = current_app.config.get("SECRET_KEY")
        payload = jwt.decode(access_token, key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        error = "Access token expired. Please log in again."
        return Result.Fail(error)
    except jwt.InvalidTokenError:
        error = "Invalid token. Please log in again."
        return Result.Fail(error)

    # if BlacklistedToken.check_blacklist(access_token):
    #     error = "Token blacklisted. Please log in again."
    #     return Result.Fail(error)
    if not check_token(access_token):
        error = "Token blacklisted. Please log in again."
        return Result.Fail(error)

    user_dict = dict(
        public_id=payload["sub"],
        # admin=payload["admin"],
        token=access_token,
        expires_at=payload["exp"],
    )
    return Result.Ok(user_dict)
