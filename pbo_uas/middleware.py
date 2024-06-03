from django.http import HttpResponseForbidden, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from rest_framework import status

from .response import error_with_msg, error_not_logged_in
from django.http import JsonResponse
#
# class TokenAuthMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         current_url = resolve(request.path_info).url_name
#         # List of URLs to bypass authentication
#         exempt_urls = ['login']
#
#         if current_url in exempt_urls:
#             return
#
#         auth = RedisTokenAuthentication()
#         user, _ = auth.authenticate(request)
#         if user:
#             request.user = user
#         else:
#             return error_not_logged_in('you are not logged in')
