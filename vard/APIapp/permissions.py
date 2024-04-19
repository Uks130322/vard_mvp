from rest_framework.permissions import BasePermission, SAFE_METHODS

from vardapp.models import User, Access


class FileAccessPermission(BasePermission):
    """
    READER = 1 - read only
    OWNER = 2 - can do anything
    COMMENTATOR = 3 - can read and comment (comment access in CommentAccessPermission)
    EDITOR = 4 - can do anything but delete
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "CREATE":
            # all authorized users can add files
            return True

        is_reader = Access.objects.filter(user_id=request.user.id, access_type_id=1,
                                          file_id=obj.pk).exists()
        is_owner = Access.objects.filter(user_id=request.user.id, access_type_id=2,
                                        file_id=obj.pk).exists()
        is_commentator = Access.objects.filter(user_id=request.user.id, access_type_id=3,
                                               file_id=obj.pk).exists()
        is_editor = Access.objects.filter(user_id=request.user.id, access_type_id=4,
                                          file_id=obj.pk).exists()

        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_commentator, is_editor]):
            # all users with any access can see the file
            return True

        elif request.method == "DELETE":
            # only owner can delete the file
            return is_owner

        else:
            # owner and editor can edit
            return is_owner or is_editor


class GiveAccessPermission(BasePermission):
    """Only the Owner can add or change the permission"""

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return obj.file_id.user_id == request.user

        return True
