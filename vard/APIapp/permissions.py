from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q
from vardapp.models import User, Access


class DataAccessPermission(BasePermission):
    """
    For files, charts and dashboards.
    READER = 1 - read only
    OWNER = 2 - can do anything
    COMMENTATOR = 3 - can read and comment (comment access in CommentAccessPermission)
    EDITOR = 4 - can do anything but delete
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "CREATE":
            # all authorized users can add files
            return True

        is_reader = Access.objects.filter(user_id=request.user.id, access_type_id=1,owner_id=obj.user_id).exists()
        #is_owner = Access.objects.filter(user_id=request.user.id, access_type_id=2, owner_id=obj.user_id).exists()
        is_owner = request.user == obj.user_id
        is_commentator = Access.objects.filter(user_id=request.user.id, access_type_id=3,owner_id=obj.user_id).exists()
        is_editor = Access.objects.filter(user_id=request.user.id, access_type_id=4,owner_id=obj.user_id).exists()

        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_commentator, is_editor]):
            # all users with any access can see the file
            return True

        # elif request.method == "GET" or request.method == "PUT" or request.method == "PATCH":
        #     # only owner can delete the file
        #     return is_owner or is_editor

        elif request.method == "DELETE":
            # only owner can delete the file
            return is_owner

        else:
            # owner and editor can edit
            return is_owner or is_editor



class DataAccessPermissionSafe(BasePermission):
    """
    For files, charts and dashboards.
    READER = 1 - read only
    OWNER = 2 - can do anything
    COMMENTATOR = 3 - can read and comment (comment access in CommentAccessPermission)
    EDITOR = 4 - can do anything but delete
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "CREATE":
            # all authorized users can add files
            return False

        is_reader = Access.objects.filter(user_id=request.user.id, access_type_id=1,owner_id=obj.user_id).exists()
        #is_owner = Access.objects.filter(user_id=request.user.id, access_type_id=2, owner_id=obj.user_id).exists()
        is_owner = request.user == obj.user_id
        is_commentator = Access.objects.filter(user_id=request.user.id, access_type_id=3,owner_id=obj.user_id).exists()
        is_editor = Access.objects.filter(user_id=request.user.id, access_type_id=4,owner_id=obj.user_id).exists()

        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_commentator, is_editor]):
            # all users with any access can see the file
            return True

        # elif request.method == "GET" or request.method == "PUT" or request.method == "PATCH":
        #     # only owner can delete the file
        #     return is_owner or is_editor

        elif request.method == "DELETE":
            # only owner can delete the file
            return False

        else:
            # owner and editor can edit
            return False


class CommentAccessPermission(BasePermission):
    """
    READER = 1 - read only
    OWNER = 2 - can add comment
    COMMENTATOR = 3 - can add comment
    EDITOR = 4 - can add comment
    """
    def has_object_permission(self, request, view, obj):
        post = obj.file_id or obj.chart_id or obj.dashboard_id
        is_reader = Access.objects.filter(user_id=request.user.id, access_type_id=1,
                                          owner_id=post.user_id).exists()
        is_owner = request.user == post.user_id
        is_commentator = Access.objects.filter(user_id=request.user.id, access_type_id=3,
                                               owner_id=post.user_id).exists()
        is_editor = Access.objects.filter(user_id=request.user.id, access_type_id=4,
                                          owner_id=post.user_id).exists()

        if request.method == "CREATE":
            # owner or commentator or editor can add comments
            return is_owner or is_commentator or is_editor
        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_commentator, is_editor]):
            # all users with any access can see the comment
            return True
        else:
            return is_owner


def get_custom_queryset(model, request_user, kwargs):
    user_ = User.objects.get(email=request_user)
    access_owners = Access.objects.filter(Q(user_id=user_) | Q(owner_id=user_)).values('owner_id')
    if access_owners.exists() and 'pk' not in kwargs:
        users = User.objects.filter(id=access_owners[0]['owner_id'])
        for access_owner in access_owners:
            users = users.union(User.objects.filter(id=access_owner['owner_id']))
        query = model.objects.filter(user_id=users[0].id)
        for user in users:
            query = query.union(model.objects.filter(Q(user_id=user.id) | Q(user_id=user_)))
    else:
        query = model.objects.filter(user_id=user_)
    if 'pk' in kwargs:
        query = model.objects.filter(id=kwargs['pk'])
    return query

