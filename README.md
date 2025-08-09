# LMS Backend

Учебный проект: Бэкенд-сервер для LMS-системы на Django + DRF.


## 🚀 Docker Compose
домашнее задание 34.2: Docker Compose.

Для локального запуска проекта используется `docker-compose`.

###  Сервисы:
- `web`: Django + Gunicorn
- `db`: PostgreSQL
- `redis`: брокер сообщений
- `celery`: обработка фоновых задач
- `celery-beat`: планировщик периодических задач

### 📌 Команды запуска:

docker compose up --build


Проект будет доступен на:

Swagger: http://localhost:8000/swagger/

Redoc: http://localhost:8000/redoc/

API: http://localhost:8000/api/

Django admin: http://localhost:8000/admin/

# CI/CD: GitHub Actions
Настроен CI/CD с помощью GitHub Actions.

🧪 CI (тестирование)
Workflow .github/workflows/ci.yml:

Устанавливает зависимости через Poetry

Поднимает PostgreSQL

Запускает тесты: pytest

poetry run pytest
⚠️ На текущий момент автотесты отключены в deploy.yml, чтобы ускорить проверку проекта.



# CD (деплой)

Workflow .github/workflows/deploy.yml:

Запускается при push в ветку feature/deploy-lms-to-vps

Подключается по SSH к VPS

Обновляет код и перезапускает проект через docker-compose

VPS
Сервер: Yandex Cloud VPS

IP-адрес: 158.160.130.4

Переменные окружения
Файл .env

Для CI используется .env.ci

# Проверки
Линтинг: black, flake8

Тесты: pytest, pytest-django

Проверка сборки: docker build


# Дополнительно
Файл docker-compose.yaml включает все необходимые сервисы

Проект запускается в Poetry окружении (pyproject.toml)

Используется PostgreSQL, Celery, Redis, Django, DRF, JWT, Stripe


# Команды разработчика:

# Проверка PEP8:
poetry run flake8

# Проверка типов:
poetry run mypy .

# Форматирование кода:
poetry run black .

# Запуск тестов:
poetry run pytest


