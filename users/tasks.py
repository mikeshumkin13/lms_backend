from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_update_email(subject, message, recipient_list):
    """
    Отправляет email всем подписчикам курса.
    subject — тема письма,
    message — текст письма,
    recipient_list — список email адресов.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email='admin@example.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )



