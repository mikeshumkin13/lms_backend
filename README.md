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


