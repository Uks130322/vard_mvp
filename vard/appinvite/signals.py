from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers
from appuser.models import User, Access
from appinvite.models import Invite
from django.core.mail import send_mail


@receiver(post_save, sender = Invite)
def notify_invite_new_user(sender, instance, created, **kwargs):
    recipient = Invite.objects.filter(email=instance.email).values('email')
    recipients = {}
    roles = Invite.objects.filter(email=instance.email)
    for role in roles:
        for choice in role.AccessType.choices:
            if choice[0] == role.access_type_id:
                role_name=choice[1]
                recipients[role.email]=role_name

    for key, value in recipients.items():
        send_mail(
            subject='Adding to VARD team',
            message=f'User {instance.owner_id} add you to their team with role {value}. '
                    f'In first u can register youself in the vard this http://127.0.0.1:8000/api/register/ '
                    f'вот тута надо вставить постоянную в которой указан текущий ip. '
                    f'не забыть написать отказ',
            from_email='stds58@yandex.ru',
            recipient_list=[key, ],
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

    for key, value in recipients.items():
        send_mail(
            subject='Adding to VARD team',
            message=f'User {instance.owner_id} add you to their team with role {value}',
            from_email='stds58@yandex.ru',
            recipient_list=[key, ],
        )
