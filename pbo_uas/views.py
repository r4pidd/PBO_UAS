from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .auth import generate_and_save_token, delete_token
from .response import ok_with_data, error_with_msg, ok_with_msg

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        token = generate_and_save_token(user.id)

        resp = {'user_id': user.id, 'token': token}

        return ok_with_data(resp, 'login successfully!')
    else:
        return error_with_msg('invalid username or password')


@api_view(['GET'])
def logout(request):
    return delete_token(request)
