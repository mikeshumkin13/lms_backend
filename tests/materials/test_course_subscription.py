import pytest
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from materials.models import Course, CourseSubscription

User = get_user_model()


@pytest.mark.django_db
def test_is_subscribed_true():
    user = User.objects.create_user(email='test1@example.com', password='12345678')
    course = Course.objects.create(title='Test Course', owner=user)
    CourseSubscription.objects.create(user=user, course=course)

    assert course.is_subscribed(user) is True


@pytest.mark.django_db
def test_is_subscribed_false():
    user = User.objects.create_user(email='test2@example.com', password='12345678')
    course = Course.objects.create(title='Test Course', owner=user)

    assert course.is_subscribed(user) is False


@pytest.mark.django_db
def test_course_subscribe_api():
    client = APIClient()
    user = User.objects.create_user(email='test3@example.com', password='12345678')
    course = Course.objects.create(title='Test API Course', owner=user)

    response = client.post('/api/users/token/', {
        'email': 'test3@example.com',
        'password': '12345678'
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post('/api/materials/courses/subscribe/', {
        'course': course.id
    }, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert CourseSubscription.objects.filter(user=user, course=course).exists()



