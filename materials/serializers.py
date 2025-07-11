from rest_framework import serializers
from .models import Course, Lesson
from users.serializers import PaymentSerializer


class LessonSerializer(serializers.ModelSerializer):
    def validate_video_url(self, value):
        """Проверка, что ссылка на видео — с YouTube"""
        if value and "youtube.com" not in value and "youtu.be" not in value:
            raise serializers.ValidationError("Ссылка должна вести на YouTube")
        return value

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "lesson_count",
            "lessons",
            "payments",
        ]

    def get_lesson_count(self, obj):
        return obj.lessons.count()
