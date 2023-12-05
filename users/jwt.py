import jwt
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from users.models import User

from rest_framework import exceptions
import jwt

from django.conf import settings


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)

        if not auth_header:
            return None

        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")

        if len(auth_token) != 2 or auth_token[0].lower() != 'bearer':
            return None

        token = auth_token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Additional validation checks
            if 'username' not in payload:
                raise exceptions.AuthenticationFailed('Invalid token payload')

            # Retrieve user by username
            username = payload['username']
            user = User.objects.get(username=username)

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token is expired, login again')

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return None