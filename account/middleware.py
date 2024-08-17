# middleware.py

import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

class HandleMissingMediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404 and request.path.startswith(settings.MEDIA_URL):
            media_path = os.path.join(settings.MEDIA_ROOT, request.path[len(settings.MEDIA_URL):])
            if not os.path.exists(media_path):
                return HttpResponseRedirect(reverse('update_profile_2'))
        return response


from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class Redirect404Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            return redirect('/login')
        return response
