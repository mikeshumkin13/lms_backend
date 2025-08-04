from django.urls import path
from .views import (
    CourseListCreateView,
    CourseRetrieveUpdateDestroyView,
    LessonListCreateView,
    LessonRetrieveUpdateDestroyView,
    CourseSubscriptionToggleView,
)

app_name = "materials"

urlpatterns = [
    path("courses/", CourseListCreateView.as_view(), name="course-list-create"),
    path(
        "courses/<int:pk>/",
        CourseRetrieveUpdateDestroyView.as_view(),
        name="course-detail",
    ),
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyView.as_view(),
        name="lesson-detail",
    ),
    path(
        "courses/subscribe/",
        CourseSubscriptionToggleView.as_view(),
        name="course-subscribe-toggle",
    ),
]
