from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User

from .clerk import verify_clerk_token

class ClerkAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            parts = auth_header.split()

            if len(parts) != 2 or parts[0] != "Bearer":
                raise AuthenticationFailed("Invalid Authorization header")

            token = parts[1]

            payload = verify_clerk_token(token)

            if payload is None:
                raise AuthenticationFailed("Invalid or tampered token")

            clerk_id = payload.get("sub")

            if not clerk_id:
                raise AuthenticationFailed("Invalid Clerk token")

            user, _ = User.objects.get_or_create(
                clerk_id=clerk_id,
                defaults={
                    "username": clerk_id,
                    "role": "STUDENT"
                }
            )

            return user, None

        except Exception as e:
            print("❌ AUTH ERROR:", str(e))
            raise AuthenticationFailed("Authentication failed")
        
# curl https://api.clerk.dev/v1/sessions \
#   -X POST \
#   -H "Authorization: Bearer sk_test_MkuYTgnSN16t0p8EQ1m5NvT1D0dywxH7XTWwBzIQPl" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "user_id": "user_3C7HjujYm16AUpCshHTCBegqXTD"
#   }'
#
#
# curl -X POST https://api.clerk.dev/v1/sessions/sess_3C7SYh8vTibicHb0P9ECNK0nNkW/tokens \
#   -H "Authorization: Bearer sk_test_MkuYTgnSN16t0p8EQ1m5NvT1D0dywxH7XTWwBzIQPl" \
#   -H "Content-Type: application/json" \
#   -d '{}'
#   -H "Authorization: Bearer sk_test_MkuYTgnSN16t0p8EQ1m5NvT1D0dywxH7XTWwBzIQPl"
#
#
#     {"object":"token","jwt":"eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18zQzdHbnZKaTVVREVYYkQ5cmtjdXRqNHYwcXUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3NzU3MzUzNzgsImZ2YSI6Wzk5OTk5LC0xXSwiaWF0IjoxNzc1NzM1MzE4LCJpc3MiOiJodHRwczovL2NoYW1waW9uLXplYnJhLTEuY2xlcmsuYWNjb3VudHMuZGV2IiwibmJmIjoxNzc1NzM1MzA4LCJzaWQiOiJzZXNzXzNDN1NZaDh2VGliaWNIYjBQOUVDTkswbk5rVyIsInN0cyI6ImFjdGl2ZSIsInN1YiI6InVzZXJfM0M3SGp1alltMTZBVXBDc2hIVENCZWdxWFREIiwidiI6Mn0.bqYrSNE1LvB7r43a5n0qpyDHTWl-M6ZWLRLnTX-DiIQJT7lFqtU30ECn7ejf1EzROq-CcJeiqL75pNnIX5mosOcI-Hc4L2WYjxeSr063qzWChCDuactUe5JdIrsv_uaJpRG53M-Z94v11BSCmtn5TI8HwOkrcREx_36MSZ05U8cvN9vma-H0IOTM3vYceVHAjMA8ZwJKzp6EE5kyGLmCNJLmZd6Qw3IkmELGfJsd5eQAffjUvpFvv4ctMmiEg6A4JCLo7MdF_l41o3Las_RkDbUMB19UI5IUleyuXPHAyv-_iy4I926F-eeYwytm-9I6CUDuc3IzgXjmSC_ElN9Cvg"}
#
#
# curl -X POST https://api.clerk.dev/v1/sessions/sess_3C7SYh8vTibicHb0P9ECNK0nNkW/tokens/django \
#   -H "Authorization: Bearer sk_test_MkuYTgnSN16t0p8EQ1m5NvT1D0dywxH7XTWwBzIQPl" \
#   -H "Content-Type: application/json"
#
# curl -X POST https://api.clerk.dev/v1/sessions/sess_3C7SYh8vTibicHb0P9ECNK0nNkW/tokens/jtmp_3C7WtMrFb1IEDOOMs3tdTOdMUmZ \
#   -H "Authorization: Bearer sk_test_MkuYTgnSN16t0p8EQ1m5NvT1D0dywxH7XTWwBzIQPl" \
#   -H "Content-Type: application/json"