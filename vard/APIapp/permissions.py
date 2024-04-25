from rest_framework.permissions import BasePermission, SAFE_METHODS

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
