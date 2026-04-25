import jwt, datetime
from accounts.models import BlacklistedToken
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
REFRESH_SECRET = settings.REFRESH_SECRET


def create_tokens(user_id):
    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.datetime.now(datetime.timezone.utc) +
               datetime.timedelta(minutes=5)
    }
    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.datetime.now(datetime.timezone.utc) +
               datetime.timedelta(days=7)
    }
    access = jwt.encode(access_payload, SECRET_KEY, 'HS256')
    refresh = jwt.encode(refresh_payload, REFRESH_SECRET, 'HS256')
    return {'access': access, 'refresh': refresh}


def verify_token(token, secret,
                 expected_type='access'):
    try:
        payload = jwt.decode(
            token, secret, algorithms=['HS256']
        )
        if payload.get('type') != expected_type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


def refresh_access_token(refresh_token):
    if BlacklistedToken.objects.filter(token=refresh_token).exists():
        return {'error': 'Token is required'}
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=['HS256'])
        if payload.get('type') != 'refresh':
            return {'error': ''}
    except jwt.ExpiredSignatureError:
        return {'error': 'token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'invalid token'}
    BlacklistedToken.objects.get_or_create(token=refresh_token)
    return create_tokens(user_id=payload['user_id'])


if __name__ == '__main__':
    print(create_tokens(1))
