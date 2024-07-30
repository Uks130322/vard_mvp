from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers
from vardapp.models import User, Access
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
            subject='Добавление в команду Варда',
            message=f'пользователь {instance.owner_id} добавил вас в свою группу с ролью {value}',
            from_email='stds58@yandex.ru',
            recipient_list=[key, ],
        )



