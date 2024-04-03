from django.core.mail import send_mail
from django.conf import settings
from api.models import Notification
from notifications_management.notification_sender.notification_sender import NotificationSender


class EmailNotificationSender(NotificationSender):

    def generate_content(self, notification: Notification):
        caregiver = notification.caregiver.caregiver
        elderly = notification.caregiver.elderly
        caregiver_level = notification.caregiver.level.level
        sensor_alert = notification.sensor_alert

        content = (
            f"Dear {caregiver.first_name} {caregiver.last_name},\n\n"
            f"We request your assistance for {elderly.first_name} {elderly.last_name} "
            f"with a caregiver level of {caregiver_level}.\n\n"
            f"Reason: A new alert has been triggered for {elderly.first_name} "
            f"{elderly.last_name} with the following details:\n\n"
            f"Start: {sensor_alert.start}\n"
            f"Location: {sensor_alert.location}\n"
            f"State: {sensor_alert.state}\n"
            f"Measurable: {sensor_alert.measurable}\n\n"
            f"Please click on the following link to confirm "
            f"that you have received this notification and will provide the "
            f"necessary assistance.\n\n"
            f"Confirmation link: {self.generate_link(notification)}\n\n"
            f"Best regards,\n"
            f"IFT785 Project Team"
        )
        return content

    def generate_subject(self, notification: Notification):
        elderly = notification.caregiver.elderly
        caregiver_level = notification.caregiver.level.level
        subject = f"Assistance Requested for {elderly.first_name} {elderly.last_name} - Caregiver Level {caregiver_level}"
        return subject

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
