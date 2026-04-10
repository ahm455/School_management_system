# accounts/authentication.py
from rest_framework import authentication
from django.contrib.auth import get_user_model
import requests
import os

User = get_user_model()

CLERK_API_KEY = os.environ.get("CLERK_API_KEY")
CLERK_API_URL = "https://api.clerk.dev/v1"

class ClerkAuthentication(authentication.BaseAuthentication):
    """
    Authenticate requests using Clerk session ID or user ID.
    Development/testing friendly. Frontend JWT not required.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                return None
        except ValueError:
            return None

        # token can be either a session ID (sess_...) or user ID (user_...)
        if token.startswith("sess_"):
            # Fetch session info from Clerk
            url = f"{CLERK_API_URL}/sessions/{token}"
            headers = {"Authorization": f"Bearer {CLERK_API_KEY}"}
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                return None
            data = resp.json()
            clerk_id = data.get("user_id")
        elif token.startswith("user_"):
            clerk_id = token
        else:
            return None

        if not clerk_id:
            return None

        # Get or create Django user for this clerk_id
        user, _ = User.objects.get_or_create(
            clerk_id=clerk_id,
            defaults={
                "username": clerk_id,
                "full_name": clerk_id,
                "email": f"{clerk_id}@example.com",
                "role": "clerk",  # default role
            }
        )

        return (user, token)