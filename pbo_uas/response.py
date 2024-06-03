from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

SUCCESS = 0
ERROR = 7

def result(code, data, msg, status, succ):
    return Response({
        "code": code,
        "success": succ,
        "msg": msg,
        "data": data,
    }, status=status)

def ok_with_data(data, msg):
    return result(SUCCESS, data, msg, status.HTTP_200_OK, True)

def ok_with_msg(msg):
    return result(SUCCESS, None, msg, status.HTTP_200_OK, True)

def error_with_data(data, msg):
    return result(ERROR, data, msg, status.HTTP_400_BAD_REQUEST, False)

def error_with_msg(msg):
    return result(ERROR, None, msg, status.HTTP_400_BAD_REQUEST, False)

def error_not_logged_in(msg):
    return JsonResponse({
        "code": status.HTTP_401_UNAUTHORIZED,
        "success": False,
        "msg": msg,
        "data": None,
    }, safe=False)
