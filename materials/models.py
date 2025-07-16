from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    preview = models.ImageField(
        upload_to="course_previews/", null=True, blank=True, verbose_name="Превью"
    )
    description = models.TextField(verbose_name="Описание")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_courses",
        verbose_name="Владелец",
    )

    def is_subscribed(self, user):
        return self.subscriptions.filter(user=user).exists()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lesson_previews/", null=True, blank=True, verbose_name="Превью"
    )
    video_url = models.URLField(verbose_name="Ссылка на видео")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_lessons",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class CourseSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Подписчик"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс"
    )

    class Meta:
        unique_together = ('user', 'course')  # один пользователь может подписаться на курс только один раз

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"


