from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import *

def is_authenticated(request):
    if not (request.user and request.user.is_authenticated):
        return False

    try:
        request.user.user_profile
        return True
    except UserProfile.DoesNotExist:
        return False
    
class IsOwner(BasePermission):
    message = ('This page is private.')

    def has_object_permission(self, request, view, obj):
        if not is_authenticated(request):
            return False

        user = request.user.user_profile

        if type(obj) == Quiz:
            the_user = obj.course.presenter
        else:
            return False

        if user != the_user:
            raise PermissionDenied
        else:
            return True
        