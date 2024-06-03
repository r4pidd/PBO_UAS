from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .response import ok_with_msg, error_with_msg

# USER_TOKEN_KEY = 'user_tokens'
# USER_TOKEN_EXPIRES_KEY_SECOND = 3600

# Connect to Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)

# def generate_and_save_token(user_id):
#     import uuid
#     token = str(uuid.uuid4())
#     redis_client.hset(USER_TOKEN_KEY, user_id, token)
#     redis_client.expire(USER_TOKEN_KEY, USER_TOKEN_EXPIRES_KEY_SECOND)

    # return token

# def get_token(user_id):
#     return redis_client.hget(USER_TOKEN_KEY, user_id)

# def delete_token(request):
#     user_id = request.headers.get('X-User-ID')
#
#     try:
#         result = redis_client.delete(USER_TOKEN_KEY.format(user_id))
#
#         if result == 1:
#             return ok_with_msg('logout successfully')
#         else:
#             return error_with_msg('logout failed, token not found')
#     except redis.RedisError as e:
#         return error_with_msg(str(e))

# class RedisTokenAuthentication(BaseAuthentication):
#
#     def authenticate(self, request):
#         user_id = request.headers.get('X-User-ID')
#         token = request.headers.get('X-User-Token')
#
#         if not user_id or not token:
#             return None, None
#
#         stored_token = get_token(user_id)
#
#         if stored_token is None or stored_token.decode('utf-8') != token:
#             return None, None
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             raise AuthenticationFailed('User not found.')
#
#         return user, None
