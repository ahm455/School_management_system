import requests
import time
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from rest_framework.exceptions import AuthenticationFailed

from school_management.settings import CLERK_AUDIENCE, CLERK_DOMAIN


JWKS_URL = f"https://{CLERK_DOMAIN}/.well-known/jwks.json"
_jwks_cache = None
_jwks_last_fetched = 0

def get_jwks():
    global _jwks_cache, _jwks_last_fetched

    if _jwks_cache is None or time.time() - _jwks_last_fetched > 7200:
        response = requests.get(JWKS_URL, timeout=5)
        response.raise_for_status()
        _jwks_cache = response.json()
        _jwks_last_fetched = time.time()

    return _jwks_cache


def verify_clerk_token(token):
    try:
        jwks = get_jwks()

        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        if not kid:
            raise Exception("Missing 'kid'")

        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)


        if not key:
            global _jwks_cache
            _jwks_cache = None
            jwks = get_jwks()

            key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

            if not key:
                raise Exception("No matching JWKS key found")

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLERK_AUDIENCE,
            issuer=f"https://{CLERK_DOMAIN}",
        )

        clerk_id = payload.get("sub")
        if not clerk_id:
            raise Exception("Missing 'sub'")

        return payload


    except ExpiredSignatureError:

        raise AuthenticationFailed("Token expired")

    except JWTError as e:

        raise AuthenticationFailed(f"JWT Error: {str(e)}")

    except Exception as e:

        raise AuthenticationFailed(f"Unknown token error: {str(e)}")
