import requests
from jose import jwt

CLERK_DOMAIN = "champion-zebra-1.clerk.accounts.dev"
JWKS_URL = f"https://{CLERK_DOMAIN}/.well-known/jwks.json"


def verify_clerk_token(token):
    try:
        jwks = requests.get(JWKS_URL).json()
        keys = jwks.get("keys", [])

        for key in keys:
            try:
                payload = jwt.decode(
                    token,
                    key,
                    algorithms=["RS256"],
                    options={
                        "verify_aud": False,
                        "verify_iss": False,
                    },
                )
                print("✅ PAYLOAD:", payload)
                return payload
            except Exception:
                continue

        print("❌ No valid key found")
        return None

    except Exception as e:
        print("❌ JWT ERROR:", str(e))
        return None