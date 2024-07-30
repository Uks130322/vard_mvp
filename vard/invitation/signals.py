from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers
from appuser.models import User, Access
from django.core.mail import send_mail


@receiver(post_save, sender = Access)
def notify_managers_appointment(sender, instance, created, **kwargs):
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



