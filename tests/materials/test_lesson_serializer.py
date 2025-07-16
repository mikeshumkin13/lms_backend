import pytest
from django.contrib.auth import get_user_model
from materials.models import Course
from materials.serializers import LessonSerializer

User = get_user_model()


@pytest.mark.django_db
class TestLessonSerializer:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание курса",
            owner=self.user
        )

    def test_valid_youtube_url(self):
        data = {
            "title": "Valid YouTube URL",
            "description": "Тест с youtube.com",
            "video_url": "https://www.youtube.com/watch?v=abc123",
            "course": self.course.id,
            "owner": self.user.id
        }
        serializer = LessonSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_valid_youtu_be_url(self):
        data = {
            "title": "Valid youtu.be URL",
            "description": "Тест с youtu.be",
            "video_url": "https://youtu.be/abc123",
            "course": self.course.id,
            "owner": self.user.id
        }
        serializer = LessonSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_invalid_url(self):
        data = {
            "title": "Invalid URL",
            "description": "Тест с другим доменом",
            "video_url": "https://vimeo.com/123456",
            "course": self.course.id,
            "owner": self.user.id
        }
        serializer = LessonSerializer(data=data)
        assert not serializer.is_valid()
        assert "video_url" in serializer.errors
        assert "Ссылка должна вести на YouTube" in str(serializer.errors["video_url"])




