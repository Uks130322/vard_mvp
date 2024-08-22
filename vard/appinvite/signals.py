from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers
from appuser.models import User, Access
from appinvite.models import Invite
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender = Invite)
def notify_invite_new_user(sender, instance, created, **kwargs):
    recipient = Invite.objects.filter(email=instance.email).values('email')
    recipients = {}
    roles = Invite.objects.filter(email=instance.email)
    for role in roles:
        recipients['id'] = role.id
        for choice in role.AccessType.choices:
            if choice[0] == role.access_type_id:
                role_name=choice[1]
                send_mail(
                    subject='Adding to VARD team',
                    message=f'User {instance.owner_id} add you to their team with role {role_name}. '
                            f'In first u can register youself in the vard this http://{settings.CURRENT_HOST}/api/register/ '
                            f'ссылка для отказа http://{settings.CURRENT_HOST}/api/invite/{role.id}',
                    from_email=settings.SERVER_EMAIL,
                    recipient_list=[role.email, ],
                )


@receiver(post_save, sender = Access)
def notify_invite_old_user(sender, instance, created, **kwargs):
    recipient = User.objects.filter(email=instance.user_id).values('email')
    recipients = {}
    users = User.objects.filter(email=instance.user_id).values('id')
    roles = Access.objects.filter(user_id__in=[users[0]['id'], ])
    for role in roles:
        for choice in role.AccessType.choices:
            if choice[0] == role.access_type_id:
                role_name=choice[1]
                recipients[role.user_id]=role_name
                send_mail(
                    subject='Adding to VARD team',
                    message=f'User {instance.owner_id} add you to their team with role {role_name} '
                            f'ссылка для отказа другая http://{settings.CURRENT_HOST}/api/access/{role.id}',
                    from_email=settings.SERVER_EMAIL,
                    recipient_list=[role.user_id, ],
                )


@receiver(post_save, sender = User)
def delete_invite_after_registration(sender, instance, created, **kwargs):
    Invite.objects.filter(email=instance.email).delete()


