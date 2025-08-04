from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def send_course_update_email_task(subject, message, recipient_list, last_updated):
    """
    Отправляет email всем подписчикам курса,
    если обновление было более 4 часов назад.
    """
    if not last_updated:
        return "Нет данных о времени обновления курса."

    time_difference = timezone.now() - timezone.datetime.fromisoformat(last_updated)

    if time_difference < timedelta(hours=4):
        print(
            "[send_course_update_email_task] Обновление курса было менее 4 часов назад. Рассылка отменена."
        )
        return "Слишком рано для повторной рассылки."

    send_mail(
        subject=subject,
        message=message,
        from_email="admin@example.com",
        recipient_list=recipient_list,
        fail_silently=False,
    )
    print(
        f"[send_course_update_email_task] Письма отправлены {len(recipient_list)} подписчикам."
    )
    return f"Письма отправлены {len(recipient_list)} подписчикам."


@shared_task
def deactivate_inactive_users_task():
    """
    Деактивирует пользователей, которые не заходили более 30 дней.
    """
    threshold = timezone.now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(is_active=True, last_login__lt=threshold)

    count = users_to_deactivate.update(is_active=False)
    print(f"[deactivate_inactive_users_task] Деактивировано пользователей: {count}")
    return count
