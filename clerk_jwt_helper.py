import requests
import os

# Your Clerk test secret key
CLERK_API_KEY = os.environ.get("CLERK_API_KEY", "sk_test_MkuYTgnSN16t0p8EQ1m5NvT1D0dywxH7XTWwBzIQPl")
USER_ID = "user_3C9fNbwd4WEvCpEZSqPkluKS5IZ"
url = "https://api.clerk.dev/v1/sessions"
headers = {
    "Authorization": f"Bearer {CLERK_API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "user_id": USER_ID
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

if "id" in data:
    print("Session created successfully!")
    print("Session ID:", data["id"])
    # JWT for your backend use (depends on Clerk setup)
    print("Use this Session ID for your backend calls or exchange for JWT if needed")
else:
    print("Error creating session:", data)