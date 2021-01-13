from rest_framework import permissions

from Account.models import MyUser
from ResponseHandle import exception_handler

from Account.models import SystemAccess


class IsAdminAuth(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        if request.user.role_id.role_type=='admin':
            return request.user
        return not request.user


def IsUserWrite(user_id):
    try:
       sys = SystemAccess.objects.get(id=user_id)
    except SystemAccess.DoesNotExist:
        output =  'system user id does not exist'
        return output
    if sys.is_add=='inactive':
        output = 'permission denied'
        return output


def IsUserDelete(user_id):
    try:
       sys = SystemAccess.objects.get(id=user_id)
    except SystemAccess.DoesNotExist:
        output =  'system user id does not exist'
        return output
    if sys.is_delete=='inactive':
        output = 'permission denied'
        return output


def IsUserUpdate(user_id):
    try:
       sys = SystemAccess.objects.get(id=user_id)
    except SystemAccess.DoesNotExist:
        output =  'system user id does not exist'
        return output
    if sys.is_update=='inactive':
        output = 'permission denied'
        return output


def IsUserRead(user_id):
    try:
       sys = SystemAccess.objects.get(id=user_id)
    except SystemAccess.DoesNotExist:
        output =  'system user id does not exist'
        return output
    if sys.is_read=='inactive':
        output = 'permission denied'
        return output