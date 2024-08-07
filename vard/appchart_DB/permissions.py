from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q

from appuser.models import Access, User


class DataAccessPermission(BasePermission):
    """
    For files, charts and dashboards.
    READER = 1 - read only
    OWNER = 2 - can do anything
    COMMENTATOR = 3 - can read and comment (comment access in CommentAccessPermission)
    EDITOR = 4 - can do anything but delete
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method == "POST":
            # all authorized users can add files
            return True

        is_reader = Access.objects.filter(user_id=request.user.id, access_type_id=1,
                                          owner_id=obj.user_id).exists()
        is_owner = request.user == obj.user_id
        is_commentator = Access.objects.filter(user_id=request.user.id, access_type_id=3,
                                               owner_id=obj.user_id).exists()
        is_editor = Access.objects.filter(user_id=request.user.id, access_type_id=4,
                                          owner_id=obj.user_id).exists()

        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_commentator, is_editor]):
            # all users with any access can see the file
            return True

        elif request.method == "DELETE":
            # only owner can delete the file
            return is_owner

        else:
            # owner and editor can edit
            return is_owner or is_editor




class DataAccessPermissionSafe(BasePermission):
    """
    For files, charts and dashboards with no editing, just create and SAFE_METHODS.
    READER = 1 - read only
    OWNER = 2 - can do anything
    COMMENTATOR = 3 - can read and comment (comment access in CommentAccessPermission)
    EDITOR = 4 - can do anything but delete
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method == "POST":
            # shouldn't be accessed, but it doesn't work here, should be in has_permission
            return False

        is_reader = Access.objects.filter(user_id=request.user.id, access_type_id=1,
                                          owner_id=obj.user_id).exists()
        is_owner = request.user == obj.user_id
        is_commentator = Access.objects.filter(user_id=request.user.id, access_type_id=3,
                                               owner_id=obj.user_id).exists()
        is_editor = Access.objects.filter(user_id=request.user.id, access_type_id=4,
                                          owner_id=obj.user_id).exists()

        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_commentator, is_editor]):
            # all users with any access can see the file
            return True

        else:
            # edit or delete are forbidden
            return False


def get_custom_queryset(model, request_user, kwargs):
    """Get custom queryset for files, charts and dashboards. Superuser have access to all files"""
    user_ = User.objects.get(email=request_user)
    if user_.is_superuser:
        return model.objects.all()
    access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
    if access_owners.exists() and 'pk' not in kwargs:
        list_access_owner = []
        for access_owner in access_owners:
            list_access_owner.append(access_owner['owner_id'])
        users = User.objects.filter(id__in=list_access_owner)
        query = model.objects.filter(user_id__in=users)
    else:
        query = model.objects.filter(user_id=user_)
    if 'pk' in kwargs:
        query = model.objects.filter(id=kwargs['pk'])
    return query





