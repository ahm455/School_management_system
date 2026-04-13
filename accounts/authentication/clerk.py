import requests
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from decouple import Config , RepositoryEnv
from school_management.settings import env_path

config = Config(RepositoryEnv(env_path))

CLERK_DOMAIN = "champion-zebra-1.clerk.accounts.dev"
JWKS_URL = f"https://{CLERK_DOMAIN}/.well-known/jwks.json"

CLERK_AUDIENCE =  config('CLERK_FRONTEND_API')

_jwks_cache = None


def get_jwks():
    global _jwks_cache

    if _jwks_cache is None:
        response = requests.get(JWKS_URL)
        response.raise_for_status()
        _jwks_cache = response.json()

    return _jwks_cache


def verify_clerk_token(token):
    try:
        jwks = get_jwks()

        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            raise Exception("Missing 'kid' in token header")

        key = next(
            (k for k in jwks["keys"] if k["kid"] == kid),
            None
        )

        if not key:
            raise Exception("No matching JWKS key found")

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLERK_AUDIENCE,
            issuer=f"https://{CLERK_DOMAIN}",
        )

        if "sub" not in payload:
            raise Exception("Missing 'sub' in token")

        if "exp" not in payload:
            raise Exception("Missing 'exp' in token")

        return payload

    except ExpiredSignatureError:
        return None

    except JWTError:
        return None

    except Exception:
        return None