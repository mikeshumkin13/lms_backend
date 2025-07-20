from rest_framework.permissions import BasePermission
from .paginators import StandardResultsSetPagination
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsModerator, IsOwnerOrModerator
from .models import Course, Lesson, CourseSubscription
from .serializers import CourseSerializer, LessonSerializer
from users.tasks import send_course_update_email_task


class Not(BasePermission):
    def __init__(self, permission):
        self.permission = permission

    def has_permission(self, request, view):
        return not self.permission.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return not self.permission.has_object_permission(request, view, obj)


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), Not(IsModerator())]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), IsModerator()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated(), Not(IsModerator())]
        return [IsAuthenticated(), IsOwnerOrModerator()]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), Not(IsModerator())]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), IsModerator()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated(), Not(IsModerator())]
        return [IsAuthenticated(), IsOwnerOrModerator()]

    def perform_update(self, serializer):
        instance = serializer.save()

        # Получаем курс, связанный с уроком
        course = instance.course

        # Получаем email всех подписчиков курса
        emails = list(course.subscribers.values_list("email", flat=True))

        if emails:
            # Вызываем Celery-задачу
            send_course_update_email_task.delay(course.id, emails)


class CourseSubscriptionToggleView(APIView):
    """
    Эндпоинт для подписки/отписки пользователя на курс.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        subscription = CourseSubscription.objects.filter(user=request.user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            CourseSubscription.objects.create(user=request.user, course=course)
            message = "Подписка оформлена"

        return Response({"message": message}, status=status.HTTP_201_CREATED)



