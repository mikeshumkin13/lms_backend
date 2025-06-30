from django.contrib.auth.models import AbstractUser
from django.conf import settings
from materials.models import Course, Lesson
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name='Урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user.email} — {self.amount} ₽ ({self.payment_method})'

