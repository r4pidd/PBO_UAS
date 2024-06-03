from django.contrib.auth import authenticate
from .response import ok_with_data, error_with_msg, ok_with_msg
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return ok_with_data(csrf_token, 'ok')

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # token = generate_and_save_token(user.id)
        token, created = Token.objects.get_or_create(user=user)

        resp = {'user_id': user.id, 'token': token.key}

        return ok_with_data(resp, 'login successfully!')
    else:
        return error_with_msg('invalid username or password')


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()

    return ok_with_msg('logout successfully!')
