from rest_framework.permissions import BasePermission, SAFE_METHODS

from appuser.models import Access


class CommentAccessPermission(BasePermission):
    """
    READER = 1 - read only
    OWNER = 2 - can add comment
    COMMENTATOR = 3 - can add comment
    EDITOR = 4 - can add comment
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        post = obj.file_id or obj.chart_id or obj.dashboard_id
        is_reader = Access.objects.filter(user_id=request.user, access_type_id=1,
                                          owner_id=post.user_id).exists()
        is_owner = request.user == post.user_id
        is_commentator = Access.objects.filter(user_id=request.user, access_type_id=3,
                                               owner_id=post.user_id).exists()
        is_editor = Access.objects.filter(user_id=request.user, access_type_id=4,
                                          owner_id=post.user_id).exists()

        if request.method == "POST":
            # processing in View by using function can_comment
            pass
        if request.method in SAFE_METHODS and any([is_reader, is_owner, is_commentator, is_editor]):
            # all users with any access can see the comment
            return True
        else:
            return is_owner or request.user == obj.user_id

def can_comment(request, data):
    """Check if user can comment"""
    post = data['file_id'] or data['chart_id'] or data['dashboard_id']
    is_reader = Access.objects.filter(user_id=request.user, access_type_id=1,
                                      owner_id=post.user_id).exists()
    is_owner = request.user == post.user_id
    is_commentator = Access.objects.filter(user_id=request.user, access_type_id=3,
                                           owner_id=post.user_id).exists()
    is_editor = Access.objects.filter(user_id=request.user, access_type_id=4,
                                      owner_id=post.user_id).exists()
    return any([is_owner, is_commentator, is_editor])
