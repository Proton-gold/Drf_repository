from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.jwt_utils import verify_token, SECRET_KEY
from accounts.models import User


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class JWTAuthentication(TokenAuthentication):
    def authenticate(self, request):
        header = request.headers.get("Authorization")
        if not header: return None
        try:
            type_, token = header.split()
        except ValueError:
            raise AuthenticationFailed("Not correctly")
        if type_.lower() != "bearer":
            raise AuthenticationFailed("Bearer in upper")
        payload = verify_token(token, SECRET_KEY, 'access')
        if not isinstance(payload, dict):
            raise AuthenticationFailed("Not correctly")
        user = User.objects.get(pk=payload['user_id'])
        return user, None
