# accounts/authentication.py
from rest_framework import authentication
from django.contrib.auth import get_user_model

User = get_user_model()

class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None  # DRF will respond with 401

        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                return None
        except ValueError:
            return None

        # Decode JWT without verifying signature (for local testing only)
        import jwt
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
        except Exception:
            return None

        clerk_id = payload.get("sub")
        if not clerk_id:
            return None

        user, _ = User.objects.get_or_create(
            clerk_id=clerk_id,
            defaults={
                "username": payload.get("email", clerk_id),
                "email": payload.get("email", ""),
                "role": "clerk",
            }
        )

        return (user, token)