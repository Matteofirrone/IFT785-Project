from django.core.mail import send_mail
from django.conf import settings
from api.models import Notification
from notifications_management.notification_sender.notification_sender import NotificationSender


class EmailNotificationSender(NotificationSender):

    def get_recipient(self, notification: Notification):
        recipient = notification.caregiver.caregiver.email
        return recipient

    def send(self, subject, content, recipient):
        send_mail(
            subject=subject,
            message=content,
            from_email=settings.EMAIL_FROM,
            recipient_list=[recipient],
            fail_silently=False,
        )
