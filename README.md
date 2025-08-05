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
35.2 CI/CD и GitHub Actions

Реализовано:
Настроен workflow .github/workflows/deploy.yml

Автозапуск деплоя при пуше в ветку feature/deploy-lms-to-vps

Деплой на VPS (Yandex Cloud) через SSH и docker-compose

Деплой выполняется по SSH с помощью appleboy/ssh-action

 - Docker Compose работает локально

 - Проект развёрнут на VPS

 - GitHub Actions автоматически деплоит на сервер

 - CI-тесты временно отключены (для ускорения сдачи)

